from sqlalchemy import Column, Integer, String, Float, BigInteger
from app.database.database import Base

class CryptoHistoricalPrice(Base):
    __tablename__ = "crypto_historical_prices"

    id = Column(Integer, primary_key=True, index=True)
    crypto_symbol = Column(String(10), nullable=False)  # Símbolo (BTC, ETH)
    timestamp = Column(BigInteger, nullable=False)  # Fecha en milisegundos
    open = Column(Float, nullable=False)  # Precio de apertura
    high = Column(Float, nullable=False)  # Precio más alto
    low = Column(Float, nullable=False)  # Precio más bajo
    close = Column(Float, nullable=False)  # Precio de cierre
    volume = Column(Float, nullable=False)  # Volumen negociado
    interval = Column(String(5), nullable=False)  # Intervalo ('1d', '1w')