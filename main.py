from fastapi import FastAPI,Depends,HTTPException,status
from models import User
import models
from db import engine,
from sqlalchemy.orm import Session
from pydantic import BaseModel #for validation
app = FastAPI()

@app.get("/user/")
async def user():
    return {"msg":"user"}

@app.post("/api/v1/add_user")
async def add_user(user:User):
    return {"username":user.username}