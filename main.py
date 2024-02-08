from typing import Annotated
from fastapi import FastAPI,Depends,status,HTTPException
import models
from db import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel #for validation


app = FastAPI()
models.base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str
    email:str
    phone:str
    password:str
    confirm_password: str
    
def get_db():
    db=SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
    
@app.post("/api/v1/users",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase, db:db_dependency):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password do not match")
    
    # db_user = models.User(**user.model_dump())
    db_user = models.User(username=user.username, email=user.email, phone=user.phone, password=user.password,confirm_password=user.confirm_password)
    db.add(db_user)
    
    db.commit()

