from datetime import datetime

import httpx
from sqlalchemy.orm import Session

from app.models.crypto import Crypto
from app.models.crypto_historical_price import CryptoHistoricalPrice

class CryptoService:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"

    async def get_crypto_price_from_api(self, symbol: str):
        url = f"{self.base_url}/ticker/price?symbol={symbol}USDT"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "symbol": symbol,
                    "price": float(data["price"])
                }
            else:
                return None

    async def get_crypto_info_from_api(self, symbol: str):
        url = f"{self.base_url}/ticker/24hr?symbol={symbol}USDT"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "name": symbol,
                    "price": float(data["lastPrice"]),
                    "last_updated": datetime.utcnow()
                }
            return None

    async def get_historical_data_service(self, symbol: str, interval: str, limit: int = 1000):
        url = f"{self.base_url}/klines?symbol={symbol}&interval={interval}&limit={limit}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "timestamp": entry[0],
                        "open": float(entry[1]),
                        "high": float(entry[2]),
                        "low": float(entry[3]),
                        "close": float(entry[4]),
                        "volume": float(entry[5]),
                    }
                    for entry in data
                ]
            else:
                raise Exception(f"Error fetching historical data: {response.text}")

    async def save_historical_data_to_db(self, symbol: str, interval: str, db: Session = None):
        historical_data = await self.get_historical_data_service(symbol, interval, limit=1000)
        for data in historical_data:
            exists = db.query(CryptoHistoricalPrice).filter_by(
                crypto_symbol=symbol,
                timestamp=data["timestamp"],
                interval=interval
            ).first()
            if not exists:
                db_record = CryptoHistoricalPrice(
                    crypto_symbol=symbol,
                    timestamp=data["timestamp"],
                    open=data["open"],
                    high=data["high"],
                    low=data["low"],
                    close=data["close"],
                    volume=data["volume"],
                    interval=interval,
                )
                db.add(db_record)
        db.commit()

    async def delete_crypto_and_historical_data(self, symbol: str, db: Session = None):
        db.query(CryptoHistoricalPrice).filter_by(crypto_symbol=symbol).delete()
        db.query(Crypto).filter_by(symbol=symbol).delete()
        db.commit()