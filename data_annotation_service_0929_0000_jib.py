# 代码生成时间: 2025-09-29 00:00:59
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional


# Pydantic模型用于数据标注的信息
class Annotation(BaseModel):
    id: int
    text: str
    label: str


# 创建FastAPI应用
app = FastAPI()


# 模拟数据库存储标注数据
annotations_db = {
    # 示例数据，实际应用中会从数据库加载
    1: {
        "id": 1,
        "text": "This is a sample text for annotation.",
        "label": "positive"
    },
    2: {
        "id": 2,
        "text": "This is another sample text.",
        "label": "negative"
    },
}


# 获取所有标注数据的端点
@app.get("/annotations")
async def read_annotations():
    return list(annotations_db.values())


# 创建一个新的标注数据的端点
@app.post("/annotations/")
async def create_annotation(annotation: Annotation):
    new_id = max(annotations_db.keys()) + 1
    annotations_db[new_id] = annotation.dict()
    return annotations_db[new_id]


# 获取单个标注数据的端点
@app.get("/annotations/{annotation_id}")
async def read_annotation(annotation_id: int):
    if annotation_id in annotations_db:
        return annotations_db[annotation_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )


# 更新一个标注数据的端点
@app.put("/annotations/{annotation_id}")
async def update_annotation(annotation_id: int, annotation: Annotation):
    if annotation_id in annotations_db:
        annotations_db[annotation_id].update(annotation.dict())
        return annotations_db[annotation_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )


# 删除一个标注数据的端点
@app.delete("/annotations/{annotation_id}")
async def delete_annotation(annotation_id: int):
    if annotation_id in annotations_db:
        return {
            "detail": f"Annotation {annotation_id} has been deleted"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )


# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        },
    )
