from app.core.config import settings
from typing import Dict
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.crud.crud_users import user_crud
import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str):
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt=salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8")
    )

def create_user_token(data: Dict):
    to_encode = data.copy()
    time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(time)
    to_encode.update({"exp": int(time.timestamp())})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

async def get_email_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        email = payload.get("sub")
        if not email: 
            raise HTTPException(401, "Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Auth_token time expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

