from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.models.user_model import User
from app.auth.jwt_handler import signJwt, decodeJwt
from app.schemas import user_schema
from app.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def signup_user(self, user_data: user_schema.UserCreate):
        if self.repo.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(username=user_data.username, email=user_data.email, password=hashed_password)
        created_user = self.repo.create_user(new_user)
        return {"message": "User created", "user": created_user}

    def login_user(self, user_data: user_schema.UserLogin):
        db_user = self.repo.get_user_by_email(user_data.email)
        if not db_user or not pwd_context.verify(user_data.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return signJwt(db_user.id)


    def get_user_by_id(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_all_users(self):
        return self.repo.get_all_users()

    def update_user(self, user_id: int, updates: user_schema.UserUpdate):
        db_user = self.repo.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = updates.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])
        return self.repo.update_user(db_user, update_data)

    def delete_user(self, user_id: int, logged_in_user_id: int):
        db_user = self.repo.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.id == logged_in_user_id:
            raise HTTPException(status_code=403, detail="Cannot delete your own account")
        self.repo.delete_user(db_user)
        return {"message": f"User with ID {user_id} deleted"}
