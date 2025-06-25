from pydantic import EmailStr, Field
from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base 


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String(50),unique=True)
    email = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=True) 
