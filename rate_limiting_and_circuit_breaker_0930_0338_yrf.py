# 代码生成时间: 2025-09-30 03:38:25
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.limiter import RateLimiter
from fastapi.limiter.starlette import StarletteLimiter
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

# Pydantic model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# API限流
limiter = RateLimiter(key_func=lambda: "openai")

# 熔断器
class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    def __init__(self, max_requests: int = 5, timeout: int = 10) -> None:
        self.max_requests = max_requests
        self.timeout = timeout
        self.requests = 0
        self.last_timeout = 0

    async def dispatch(self, request: Request, call_next) -> Response:
        if self.requests > self.max_requests:
            if (request.timestamp() - self.last_timeout) < self.timeout:
                raise StarletteHTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service is currently unavailable.")
            else:
                self.requests = 0
                self.last_timeout = 0
        
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            self.requests += 1
            self.last_timeout = request.timestamp()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

app.add_middleware(CircuitBreakerMiddleware)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/items/")
@limiter.limit("5/minute")
async def read_items():
    """
    Get list of items.
    Use this endpoint to get all items.
    """
    return {"message": "Hello World"}

@app.post("/items/")
@limiter.limit("5/minute")
async def create_item(item: Item):
    """
    Create an item.
    Use this endpoint to create an item.
    """
    return item