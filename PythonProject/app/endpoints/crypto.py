# app/predictor/prediction_service.py
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.models.crypto_historical_price import CryptoHistoricalPrice
from app.services.external_crypto import ExternalCryptoService


class PredictionService:
    def __init__(self):
        self.external_crypto_service = ExternalCryptoService()

    def calculate_rsi(self, series, window):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def get_historical_data(self, symbol: str, db_session: Session, timeframe: str = '1d'):
        historical_data = db_session.query(CryptoHistoricalPrice).filter(
            CryptoHistoricalPrice.crypto_symbol == symbol,
            CryptoHistoricalPrice.interval == timeframe
        ).order_by(CryptoHistoricalPrice.timestamp).all()

        if not historical_data:
            raise Exception(f"No historical data found for {symbol} with timeframe {timeframe}")

        df = pd.DataFrame([{
            "timestamp": data.timestamp,
            "close": float(data.close),
            "volume": float(data.volume)
        } for data in historical_data])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def add_technical_indicators(self, df):
        df['SMA_10'] = df['close'].rolling(window=10).mean()
        df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
        df['RSI'] = self.calculate_rsi(df['close'], window=14)
        return df

    async def get_external_data(self, symbol: str):
        news_sentiment = await self.external_crypto_service.fetch_news_from_google(symbol)
        sentiment_mapping = {
            "neutral": 0,
            "positive": 1,
            "negative": -1
        }
        numeric_sentiments = [sentiment_mapping.get(item['sentiment'], 0) for item in news_sentiment]
        average_sentiment = np.mean(numeric_sentiments)
        return average_sentiment

    def prepare_features(self, df, news_sentiment):
        df['news_sentiment'] = news_sentiment
        for col in ['close', 'volume', 'SMA_10', 'EMA_10', 'RSI', 'news_sentiment']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.fillna(method='bfill').fillna(method='ffill')
        X = df[['close', 'volume', 'SMA_10', 'EMA_10', 'RSI', 'news_sentiment']].values
        y = df['close'].shift(-1).dropna().values
        return X, y

    def determine_action(self, current_price, predicted_price, threshold=0.05):
        if isinstance(predicted_price, list):
            predicted_price = np.mean(predicted_price)
        change_percent = (predicted_price - current_price) / current_price
        if change_percent > threshold:
            return "comprar"
        elif change_percent < -threshold:
            return "vender"
        else:
            return "aguantar"

    async def predict_crypto_price(self, symbol: str, timeframe: str, db_session: Session):
        try:
            df = pd.DataFrame()
            if timeframe == "short":
                df = self.get_historical_data(symbol, db_session, '1d')
            elif timeframe == "long":
                df = self.get_historical_data(symbol, db_session, '1w')
            df = self.add_technical_indicators(df)
            news_sentiment = await self.get_external_data(symbol)
            X, y = self.prepare_features(df, news_sentiment)

            if len(X) < 10:
                raise Exception("Not enough historical data for prediction")

            if timeframe == "short":
                split_index = int(len(df) * 0.8)
                X_train, X_test = X[:split_index], X[split_index:]
                y_train, y_test = y[:split_index], y[split_index:]

                if len(X_test) == 0:
                    raise Exception("No data available for prediction. Insufficient historical data.")

                model = LinearRegression()
                model.fit(X_train, y_train)
                predicted_price = model.predict(X_test[-1].reshape(1, -1))[0]

            elif timeframe == "long":
                model = ARIMA(df['close'], order=(5, 1, 0))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=30)
                predicted_price = forecast.mean()

            else:
                raise Exception("Invalid timeframe specified")

            current_price = df['close'].iloc[-1]
            action = self.determine_action(current_price, predicted_price)

            return {"symbol": symbol, "timeframe": timeframe, "prediction": predicted_price, "action": action}
        except Exception as e:
            raise Exception(f"Error in prediction: {str(e)}")