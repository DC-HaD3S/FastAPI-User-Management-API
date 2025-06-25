from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
from app.auth.jwt_handler import decodeJwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = decodeJwt(jwtoken)
        return bool(payload)
