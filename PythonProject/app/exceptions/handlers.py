from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.exceptions.custom_exceptions import RateLimitExceededException

async def rate_limit_handler(request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Has excedido el límite de peticiones. Intenta más tarde."},
    )
