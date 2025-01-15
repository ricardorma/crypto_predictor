from fastapi import HTTPException

class RateLimitExceededException(HTTPException):
    def __init__(self):
        super().__init__(status_code=429, detail="Has excedido el límite de peticiones. Intenta más tarde.")
