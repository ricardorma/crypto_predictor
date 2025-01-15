from pydantic import BaseModel

class CryptoBase(BaseModel):
    symbol: str

class CryptoCreate(CryptoBase):
    pass

class CryptoUpdate(BaseModel):
    name: str = None
    price: float = None