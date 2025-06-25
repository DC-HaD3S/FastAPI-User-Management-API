from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: Optional[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserDelete(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "rohit@example.com"
            }
        }
