# 代码生成时间: 2025-10-10 03:27:23
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from random import choice, randint, seed
from faker import Faker

app = FastAPI()
fake = Faker()

class MockData(BaseModel):
    id: int = Field(..., description="The identifier of the mock data")
    name: str = Field(..., description="The name of the mock data")
    age: int = Field(..., description="The age of the mock data")
    gender: str = Field(..., description="The gender of the mock data")
    email: str = Field(..., description="The email of the mock data")

@app.get("/mock-data/", response_model=MockData, description="Generate a single mock data")
def read_mock_data():
    return MockData("id": randint(1, 1000),
                  "name": fake.name(),
                  "age": randint(18, 65),
                  "gender": choice(["Male", "Female", "Other"]),
                  "email": fake.email())

@app.get("/mock-data/list/", response_model=List[MockData], description="Generate a list of mock data")
def read_mock_data_list():
    return [MockData("id": randint(1, 1000),
                   "name": fake.name(),
                   "age": randint(18, 65),
                   "gender": choice(["Male", "Female", "Other"]),
                   "email": fake.email()) for _ in range(10)]

@app.exception_handler(ValueError)
def value_error_handler(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)