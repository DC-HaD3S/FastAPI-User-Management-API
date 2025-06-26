from fastapi import Depends, HTTPException
from app.auth.jwt_handler import decodeJwt
from app.auth.jwt_bearer import JWTBearer


def get_current_user_id(token: str = Depends(JWTBearer())) -> int:
    payload = decodeJwt(token)
    if not payload or "userID" not in payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    try:
        return int(payload["userID"])
    except (KeyError, ValueError, TypeError):
        raise HTTPException(status_code=403, detail="Invalid or expired token")

