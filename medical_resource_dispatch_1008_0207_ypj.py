# 代码生成时间: 2025-10-08 02:07:20
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional


# Pydantic模型定义
class MedicalResourceRequest(BaseModel):
    name: str
    quantity: int
    description: Optional[str] = Field(default=None, description="Optional description of the resource")


# 创建FastAPI应用
app = FastAPI()


# 存储医疗资源的示例数据库
medical_resources_db = {
    "medication": {
        "name": "Medication",
        "quantity": 100,
        "description": "Generic medication"
    }
}


# 创建医疗资源调度的端点
@app.post("/dispatch/medical_resources/")
async def dispatch_medical_resources(resource: MedicalResourceRequest):
    """
    Endpoint to dispatch medical resources.
    Returns the dispatched resource with the updated quantity.
    """
    # 检查输入的资源名称是否已存在于数据库中
    if resource.name not in medical_resources_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The resource {resource.name} is not available."
        )
    
    # 更新数据库中的资源数量
    resource_in_db = medical_resources_db[resource.name]
    resource_in_db["quantity"] -= resource.quantity
    
    # 添加错误处理来确保数量不会变成负数
    if resource_in_db["quantity"] < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough resources. Only {resource_in_db['quantity']} are available."
        )
    
    # 返回更新后的资源状态
    return {
        "name": resource_in_db["name"],
        "quantity": resource_in_db["quantity"],
        "description": resource_in_db["description"]
    }


# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
