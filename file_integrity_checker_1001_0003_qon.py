# 代码生成时间: 2025-10-01 00:03:11
from fastapi import FastAPI, HTTPException, StatusCode
from pydantic import BaseModel, ValidationError
from typing import Optional
import hashlib


app = FastAPI()

class FileChecksum(BaseModel):
    """Model for file checksum request."""
    filename: str
    checksum: str

    @classmethod
    def from_json(cls, json_data: dict) -> 'FileChecksum':
        """Class method to create an instance from JSON data."""
        try:
            return cls(**json_data)
        except ValidationError as exc:
            raise HTTPException(
                status_code=StatusCode.BAD_REQUEST,
                detail=str(exc)
            )

@app.post("/check")
async def check_file_integrity(file_checksum: FileChecksum):
    "