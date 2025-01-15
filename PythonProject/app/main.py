import uvicorn
from fastapi import FastAPI
from app.endpoints import crypto

from app.models.crypto import Base
from app.database.database import engine

app = FastAPI(
    title="Crypto Tracker API",
    description="API destinada a la consulta y predicción de precios de criptomonedas",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# Incluir el router de criptomonedas
app.include_router(crypto.router, prefix="/api/v1/crypto")


@app.get("/ping")
async def ping():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)