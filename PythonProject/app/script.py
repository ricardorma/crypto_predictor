from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.crypto import Crypto  # Cambia según tu estructura de carpetas

DATABASE_URL = "postgresql://crypto_user:crypto_password@localhost:5432/crypto_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Agrega criptomonedas de ejemplo
def populate_database():
    session = SessionLocal()
    try:
        cryptos = [
            Crypto(symbol="BTC", name="Bitcoin", price=45000.00),
            Crypto(symbol="ETH", name="Ethereum", price=3000.00),
            Crypto(symbol="XRP", name="Ripple", price=0.50),
        ]
        session.add_all(cryptos)
        session.commit()
        print("Criptomonedas insertadas exitosamente")
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_database()
