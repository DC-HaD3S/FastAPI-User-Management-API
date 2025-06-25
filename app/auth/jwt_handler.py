import time
import jwt
from decouple import config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
JWT_SECRET = config("secret", default="default_secret_key")
JWT_ALGORITHM = config("algorithm", default="HS256")

def token_response(token: str):
    return {
        "access_token": token
    }

def signJwt(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 500  # expires in 500 seconds
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # Check if token is still valid
        return decoded_token if decoded_token.get("expiry", 0) >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
