from argon2 import PasswordHasher
import jwt
from datetime import datetime, timezone, timedelta
from app.config import settings

ph = PasswordHasher()


def hash_password(password):
    hash = ph.hash(password)
    return hash


def verify_password(plain: str, hashed: str):
    return ph.verify(hashed, plain)


def create_access_token(user_id):
    encoded = jwt.encode(
        {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        settings.secret_key,
        algorithm="HS256",
    )
    return encoded


def decode_access_token(token):
    return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
