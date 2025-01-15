# app/endpoints/crypto.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.crypto_service import CryptoService
from app.services.external_crypto import ExternalCryptoService
from app.predictor.prediction_service import PredictionService

class CryptoEndpoints:
    def __init__(self):
        self.router = APIRouter()
        self.crypto_service = CryptoService()
        self.external_crypto_service = ExternalCryptoService()
        self.predictor = PredictionService()
        self.add_routes()

    def add_routes(self):
        self.router.add_api_route("/cryptos/{symbol}", self.delete_crypto, methods=["DELETE"])
        self.router.add_api_route("/cryptos/{symbol}/realtime", self.get_crypto_realtime_price, methods=["GET"])
        self.router.add_api_route("/cryptos/{symbol}/predict", self.predict_price, methods=["GET"], dependencies=[Depends(get_db)])
        self.router.add_api_route("/cryptos/{symbol}/historical", self.fetch_and_store_historical_data, methods=["POST"], dependencies=[Depends(get_db)])
        self.router.add_api_route("/cryptos/{symbol}/trends", self.get_crypto_trends, methods=["GET"])
        self.router.add_api_route("/cryptos/{symbol}/mentions", self.get_social_mentions, methods=["GET"])
        self.router.add_api_route("/cryptos/{symbol}/news", self.get_crypto_news, methods=["GET"])

    async def delete_crypto(self, symbol: str):
        await self.crypto_service.delete_crypto_and_historical_data(symbol)
        return {"detail": f"Crypto {symbol} deleted successfully"}

    async def get_crypto_realtime_price(self, symbol: str):
        price_data = await self.crypto_service.get_crypto_price_from_api(symbol)
        if price_data is None:
            raise HTTPException(status_code=404, detail="Price data not found")
        return price_data

    async def predict_price(self, symbol: str, timeframe: str, db: Session = Depends(get_db)):
        try:
            prediction = await self.predictor.predict_crypto_price(symbol, timeframe, db)
            return prediction
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def fetch_and_store_historical_data(self, symbol: str, db: Session = Depends(get_db)):
        try:
            await self.crypto_service.save_historical_data_to_db(symbol, "1d", db)
            await self.crypto_service.save_historical_data_to_db(symbol, "1w", db)
            return {"detail": f"Historical data for {symbol} saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_crypto_trends(self, symbol: str, timeframe: str = "today 12-m"):
        try:
            trends = self.external_crypto_service.fetch_google_trends_data(symbol, timeframe)
            if not trends:
                raise HTTPException(status_code=404, detail="No se encontraron datos de tendencias.")
            return {"symbol": symbol, "trends": trends}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener tendencias: {str(e)}")

    async def get_social_mentions(self, symbol: str, max_results: int = 10):
        try:
            mentions = await self.external_crypto_service.fetch_reddit_data(symbol, max_results)
            if not mentions:
                raise HTTPException(status_code=404, detail="No se encontraron menciones.")
            return {"symbol": symbol, "mentions": mentions}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener menciones: {str(e)}")

    async def get_crypto_news(self, symbol: str, max_results: int = 10):
        try:
            news = await self.external_crypto_service.fetch_news_from_google(symbol, max_results)
            if not news:
                raise HTTPException(status_code=404, detail="No se encontraron noticias.")
            return {"symbol": symbol, "news": news}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener noticias: {str(e)}")

crypto_endpoints = CryptoEndpoints()
router = crypto_endpoints.router