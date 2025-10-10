# 代码生成时间: 2025-10-10 22:24:48
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# Pydantic model for votes
class Vote(BaseModel):
    option: str
    user_id: str

# Pydantic model for vote options
class VoteOption(BaseModel):
    option: str

# Initialize the FastAPI application
app = FastAPI()

# In-memory store for options and votes
vote_options = []
votes = []

@app.post("/options/")
async def add_option(option: VoteOption):
    vote_options.append(option)
    return option

@app.post("/vote/")
async def vote(vote: Vote):
    try:
        vote = vote.dict()
        vote = jsonable_encoder(vote)
        votes.append(vote)
        return vote
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@app.get("/options/")
async def read_options():
    return vote_options

@app.get("/votes/")
async def read_votes():
    return votes

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Run the application using: uvicorn voting_system:app --reload