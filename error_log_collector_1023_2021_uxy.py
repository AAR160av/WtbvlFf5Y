# 代码生成时间: 2025-10-23 20:21:47
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic模型用于错误日志数据
class ErrorLog(BaseModel):
    error_id: int
    timestamp: str
    error_message: str
    stack_trace: Optional[str] = None

# 创建FastAPI应用
app = FastAPI(title="Error Log Collector", version="0.0.1")

# HTML模板渲染
templates = Jinja2Templates(directory="templates")

# 错误日志收集器端点
@app.post("/log_error")
async def log_error(error_log: ErrorLog):
    # 将错误日志数据记录到日志
    logger.error(jsonable_encoder(error_log))
    # 返回成功响应
    return JSONResponse(content={"message": "Error logged successfully"}, status_code=status.HTTP_200_OK)

# 自定义错误处理
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    # 记录错误
    logger.error(f"ValueError: {exc}")
    # 返回错误响应
    return JSONResponse(content={"message": exc.__str__()}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# API文档端点
@app.get("/docs", include_in_schema=False)
async def redirect_to_docs():
    return HTMLResponse("Redirecting...", status_code=200)
    return await app.openapi_url()

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# HTML模板（可用于显示API文档）
# templates/index.html
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Error Log Collector</title>
# </head>
# <body>
#     <h1>Welcome to Error Log Collector</h1>
#     <p><a href="/docs">View API Docs</a></p>
# </body>
# </html>