from typing import Annotated
from fastapi import FastAPI,Depends, status,HTTPException
import models
from db import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel #for validation

app = FastAPI()
# app.include_router(auth.router)
models.base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str
    email:str
    phone:str
    password:str
    confirm_password: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
def get_db():
    db=SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
    
@app.post("/api/v1/new_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    # Check if user with the provided email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    # Check if user with the provided username already exists
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    
    existing_phone= db.query(models.User).filter(models.User.phone==user.phone).first()
    if existing_phone:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this phone exists already")
    


    # Create new user if not already exists
    db_user = models.User(username=user.username, email=user.email, phone=user.phone, password=user.password,
                          confirm_password=user.confirm_password)
    db.add(db_user)
    db.commit()
    return {"msg": "New user created successfully"}

    
    
@app.get("/api/v1/users/{user_id}",status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db:db_dependency):
    user = db.query(models.User).filter(models.User.username == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="No such user")
    return user

@app.post("/api/v1/login", status_code=status.HTTP_200_OK)
async def login_user(user_login: UserLogin, db: db_dependency):
    user_from_db = db.query(models.User).filter(models.User.email == user_login.email).first()
    if user_from_db is None or user_from_db.password != user_login.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"msg": "Login successful"}

@app.delete("/api/v1/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, user_login: UserLogin, db: db_dependency):
    user_from_db = db.query(models.User).filter(models.User.username == user_id).first()
    if user_from_db is None or user_from_db.password != user_login.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    db.delete(user_from_db)
    db.commit()
    
    return {"msg": "Login successful"}


    