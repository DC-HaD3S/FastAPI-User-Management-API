import time, jwt
from decouple import config
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def signJwt(user_id: int): 
    payload = {"userID": user_id, "expiry": time.time() + 3600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token}


def decodeJwt(token):
    if isinstance(token, str):
        token = token.encode()  
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
