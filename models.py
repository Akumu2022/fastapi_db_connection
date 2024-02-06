from pydantic import BaseModel
from sqlalchemy import Boolean,Column,Integer,String
from db import base
from passlib.hash import bcrypt
from sqlalchemy_utils.types.email import EmailType

class User(base):
    __tablename__="users"
    username = Column(String(20),nullable=False, unique=True)
    email = Column(EmailType, nullable=False, unique=True)    
    phone: Column(int,nullable=False,unique=True)
    password_hash = Column(String, nullable=False)   
    confirm_password = Column(String, nullable=False)   
    
    
    def encrypt_password(self,password):
        self.password_hash = bcrypt.hash(password)
        
    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
