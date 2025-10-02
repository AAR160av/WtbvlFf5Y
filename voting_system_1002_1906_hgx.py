# 代码生成时间: 2025-10-02 19:06:36
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

# Pydantic模型用于请求和响应数据的验证
class Vote(BaseModel):
    option_id: int
    user_id: int

# 保存投票信息的存储结构（可以替换为数据库）
votes = []

app = FastAPI()

# 初始选项列表
options = [
    {'id': 1, 'name': 'Option A'},
    {'id': 2, 'name': 'Option B'},
    {'id': 3, 'name': 'Option C'},
]

# 获取所有选项的端点
@app.get("/options/")
async def read_options():
    return options

# 提交投票的端点
@app.post("/vote/")
async def vote(vote: Vote):
    if not vote in votes:
        votes.append(vote.dict())
        return {
            "message": "Vote recorded successfully",
            "vote": vote.dict()
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User has already voted for this option.")

# 获取所有投票的端点
@app.get("/votes/")
async def read_votes():
    return votes

# 获取API文档的端点（FastAPI自动生成）
@app.get("/docs")
async def get_documentation():
    return {
        "message": "Redirect to API documentation",
        "url": f"{request.base_url}/docs"
    }
