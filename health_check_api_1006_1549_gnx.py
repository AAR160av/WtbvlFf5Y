# 代码生成时间: 2025-10-06 15:49:23
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

# Pydantic model for health check response
class HealthCheckResponse(BaseModel):
    status: str
    uptime: str

# Create the FastAPI app instance
app = FastAPI()

# Health check endpoint
@app.get("/health")
async def health_check():
    return HealthCheckResponse(status="ok", uptime="N/A")

# Error handler for 404 errors
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(content={"detail": "Not Found"}, status_code=404)

# Error handler for internal server errors
@app.exception_handler(500)
async def internal_server_exception_handler(request, exc):
    return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

# Error handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)