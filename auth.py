from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from db import SessionLocal
from models import User
from pydantic import BaseModel
from typing import Annotated


router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

SECRET_KEY = "72e0b5b1b93df4a42b5ada5f569def081ed26e10ce9d1cd259fba51c93e5b719"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer= OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]