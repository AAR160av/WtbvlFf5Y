# 代码生成时间: 2025-10-17 02:42:20
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import csv
from typing import List
import io

# Pydantic模型定义
class CSVRow(BaseModel):
    column1: str
    column2: str
    column3: str

# 创建FastAPI应用
app = FastAPI()

# 错误处理
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

# 批量处理CSV文件的端点
@app.post("/process-csv/")
async def process_csv_file(csv_files: List[UploadFile] = File(...)):
    # API文档自动生成
    processed_data = []
    for upload_file in csv_files:
        try:
            # 读取CSV文件内容
            contents = await upload_file.read()
            file_like = io.StringIO(contents.decode('utf-8'))
            reader = csv.DictReader(file_like)
            # 验证每行是否符合CSVRow模型
            for row in reader:
                valid_row = CSVRow(**row)
                processed_data.append(valid_row.dict())
        except csv.Error as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {e}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid data in CSV: {e}")

    return {"processed_data": processed_data}
