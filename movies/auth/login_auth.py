from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
from models.user import User

#app = FastAPI()

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"


class LoginData(BaseModel):
    username: str
    password: str


def login(user: User, password):
    user = user.to_dict()
    username = user['username']
    hash_pw = user['password']
    password = password.encode('utf-8')

    if not bcrypt.checkpw(password, hash_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "role": user['role']
        }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


