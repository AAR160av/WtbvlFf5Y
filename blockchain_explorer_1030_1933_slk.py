# 代码生成时间: 2025-10-30 19:33:50
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

# Pydantic模型用于API请求和响应数据验证
class BlockQuery(BaseModel):
    height: Optional[int] = None
    hash: Optional[str] = None

class BlockResponse(BaseModel):
    height: int
    hash: str
    previous_hash: str
    merkle_root: str
    timestamp: int
    transactions: list

# 创建FastAPI应用实例
app = FastAPI()

# 模拟区块链数据
blockchain_data = [
    {
        "height": 1,
        "hash": "000000000000000000000000000000001",
        "previous_hash": "0",
        "merkle_root": "00000000000000000000000000000000",
        "timestamp": 1609459200,
        "transactions": []
    },
    # ... 其他区块数据
]

# 查询区块的端点
@app.get("/block")
async def get_block(query: BlockQuery):
    """
    查询区块信息

    :param query: BlockQuery对象，包含区块的高度(height)和哈希值(hash)
    :return: 区块信息BlockResponse对象
    """
    for block in blockchain_data:
        if query.height and block["height"] == query.height:
            return BlockResponse(**block)
        elif query.hash and block["hash"] == query.hash:
            return BlockResponse(**block)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Block not found")

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    自定义错误处理
    :param request: 请求对象
    :param exc: 异常对象
    :return: 错误响应JSON
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# 遵循FastAPI最佳实践
# 1. 使用Pydantic模型进行数据验证
# 2. 自动生成API文档
# 3. 通过HTTPException处理错误
# 4. 使用JSONResponse返回错误信息
