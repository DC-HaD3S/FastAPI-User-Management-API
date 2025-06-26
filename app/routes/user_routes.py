from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.schemas.common import MessageResponse
from app.database import get_db
from app.services.user_service import UserService
from app.auth.dependencies import get_current_user_id  

router = APIRouter()

@router.post("/signup", response_model=MessageResponse)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return UserService(db).signup_user(user)

@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    return UserService(db).login_user(user)

@router.get("/users/{user_id}", response_model=user_schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return UserService(db).get_user_by_id(user_id)

@router.get("/users", response_model=list[user_schema.UserOut])
def get_users(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return UserService(db).get_all_users()

@router.put("/users/{user_id}", response_model=user_schema.UserOut)
def update_user(
    user_id: int,
    updates: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return UserService(db).update_user(user_id, updates)

@router.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return UserService(db).delete_user(user_id, current_user_id)

