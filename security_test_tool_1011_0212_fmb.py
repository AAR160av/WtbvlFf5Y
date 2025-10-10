# 代码生成时间: 2025-10-11 02:12:33
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from . import schemas, crud, main
from .database import SessionLocal

# Define a Pydantic model for the security test tool
class SecurityTestModel(BaseModel):
    input_data: str
    test_type: str

# Initialize FastAPI app
app = FastAPI()

# Security configurations
SECRET_KEY = "SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency for getting the user
async def get_user(db, username: str):
    user = crud.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user

# Dependency for getting the current active user
async def get_current_user(token: str = Depends(oauth2_scheme), scopes: Optional[SecurityScopes] = None):
    if scopes is not None and "me" not in scopes.scopes:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not enough privileges")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = jsonable_encoder(payload)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Security test tool endpoint
@app.post("/security-test")
async def security_test(input_data: str, test_type: str, db: SessionLocal = Depends(main.get_db)):
    """
    Perform a security test based on the input data and test type.
    """
    try:
        test_result = crud.perform_security_test(db, input_data, test_type)
        return JSONResponse(content={"message": "Security test completed", "result": test_result})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Error handling
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": exc.errors(),
            "body": request.body,
        }),
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "detail": exc.detail,
        }),
    )

# Generate API documentation
@app.get("/docs")
def read_docs():
    return redirect("/docs")

# OAuth2 token endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(main.get_db)):
    try:
        user = crud.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # default to 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt