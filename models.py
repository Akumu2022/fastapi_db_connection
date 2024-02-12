from pydantic import BaseModel
from sqlalchemy import Boolean,Column,Integer,String
from db import base
from passlib.hash import bcrypt
from sqlalchemy_utils.types.email import EmailType

class User(base):
    __tablename__="users"
    username = Column(String(20),primary_key=True,nullable=False,unique=True)
    email = Column(EmailType, nullable=False, unique=True)    
    phone= Column(String(13),nullable=False,unique=True)
    password = Column(String(100), nullable=False)   
