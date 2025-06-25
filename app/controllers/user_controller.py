from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app import models
from app.auth.jwt_handler import signJwt
from app.schemas.user_schema import UserCreate, UserLogin, UserUpdate, UserDelete
from fastapi.responses import JSONResponse
from fastapi import Depends
from app.auth.jwt_bearer import JWTBearer
from app.auth.jwt_handler import decodeJwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user: UserCreate, db: Session) -> dict:
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
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already exists"
        )

def get_all_users(db: Session):
    users = db.query(models.User).all()
    return users


def login_user(user: UserLogin, db: Session) -> dict:
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return signJwt(db_user.email)


def get_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def update_user(user_id: int, user: UserUpdate, db: Session):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        for key, value in user.dict(exclude_unset=True).items():
            if value is not None:
                if key == "password":
                    value = pwd_context.hash(value)
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or database error"
        )



def delete_user(user_id: int, db: Session, token: str = Depends(JWTBearer())):
    payload = decodeJwt(token)
    logged_in_email = payload.get("userID")  # Assuming userID is actually the email

    # Fetch the user to delete
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if trying to delete own account
    if user_to_delete.email == logged_in_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete your own account"
        )

    db.delete(user_to_delete)
    db.commit()
    return JSONResponse(
        content={"message": f"User with ID {user_id} deleted successfully"},
        status_code=status.HTTP_200_OK
    )

