from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from auth.jwt_handler import signJwt
import models
from database import SessionLocal, engine
from auth.bearer import jwtBearer
from passlib.context import CryptContext

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "rohit",
                "email": "roh@gmail.com",
                "password": "asdf",
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "roh@gmail.com",
                "password": "asdf"
            }
        }

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "roh",
                "email": "rohit@google.com",
                "password": "qwert"
            }
        }

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/signup", tags=["users"], status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    try:
        hashed_password = pwd_context.hash(user.password) if user.password else None
        db_user = models.User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully", "user_id": db_user.id}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

@app.post("/users/login", tags=["users"], status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return signJwt(db_user.email)

@app.get("/users/{user_id}", tags=["users"], status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency, auth: str = Depends(jwtBearer())):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.put("/users/{user_id}", tags=["users"], status_code=status.HTTP_200_OK, dependencies=[Depends(jwtBearer())])
async def update_user(user_id: int, user: UserUpdate, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        for key, value in user.dict().items():
            if value is not None:
                if key == "password":
                    value = pwd_context.hash(value)
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or database error")

@app.delete("/users/{user_id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(jwtBearer())])
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}