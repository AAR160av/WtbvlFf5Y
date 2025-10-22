# 代码生成时间: 2025-10-22 11:14:03
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import List
from fastapi.responses import JSONResponse

"""
自动批改工具的FastAPI端点实现。
"""
app = FastAPI()

# Pydantic模型定义用于提交的数据
class Submission(BaseModel):
    student_id: int
    answers: List[str]

# 错误处理器
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

# 批改作业的端点
@app.post("/grade")
async def grade(submission: Submission):
    try:
        # 模拟批改作业的逻辑
        # 这里只是一个示例，实际逻辑需要根据批改需求来定义
        grade = sum(int(answer == "correct") for answer in submission.answers)
        return {"student_id": submission.student_id, "total_grade": grade}
    except Exception as e:
        # 错误处理
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Swagger UI文档支持
@app.get("/docs")
async def swagger_ui_redirect():
    return JSONResponse(
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
        headers={"Location": "/openapi.json"}
    )

# ReDoc文档支持
@app.get("/redoc")
async def redoc_redirect():
    return JSONResponse(
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
        headers={"Location": "/openapi.json"}
    )