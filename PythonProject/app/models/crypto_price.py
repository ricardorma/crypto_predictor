from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.database import Base


class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    price = Column(Float, nullable=False)