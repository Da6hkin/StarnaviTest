from datetime import datetime, timedelta

import bcrypt
import jwt
from core.config import settings


def encode_jwt(payload: dict, secret: str = settings.jwt_secret, algorithm: str = settings.jwt_algo,
               expire_time: int = settings.jwt_expire):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_time)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded


def decode_jwt(token, secret: str = settings.jwt_secret, algorithm: str = settings.jwt_algo):
    decoded = jwt.decode(token, secret, algorithms=algorithm)
    return decoded


def hash_password(password: str, ) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
