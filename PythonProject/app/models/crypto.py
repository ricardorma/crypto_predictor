from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime

from app.database.database import Base


class Crypto(Base):
    __tablename__ = "cryptos"

    symbol = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)