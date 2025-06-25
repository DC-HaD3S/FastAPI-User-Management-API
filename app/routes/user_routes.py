from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas import user_schema
from app.controllers import user_controller
from app.database import SessionLocal
from app.auth.jwt_bearer import JWTBearer

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: user_schema.UserCreate, db: db_dependency):
    return user_controller.create_user(user, db)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: user_schema.UserLogin, db: db_dependency):
    return user_controller.login_user(user, db)

@router.get("/", status_code=200, dependencies=[Depends(JWTBearer())])
def list_users(db: Session = Depends(get_db)):
    return user_controller.get_all_users(db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_user(user_id: int, db: db_dependency):
    return user_controller.get_user(user_id, db)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_user(user_id: int, user: user_schema.UserUpdate, db: db_dependency):
    return user_controller.update_user(user_id, user, db)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    return user_controller.delete_user(user_id, db, token=token)
