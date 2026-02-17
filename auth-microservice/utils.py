import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI "Bearer" extractor
bearer_scheme = HTTPBearer(auto_error=False)


def password_hash(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=422, detail="Password too long (max 72 bytes)")
    return pwd_context.hash(password)

def compare_password(raw: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(raw, hashed)
    except Exception:
        return False


def _create_jwt(payload: Dict[str, Any], secret: str, expires_in: timedelta) -> str:
    now = datetime.now(timezone.utc)
    to_encode = dict(payload)
    to_encode["iat"] = int(now.timestamp())
    to_encode["exp"] = int((now + expires_in).timestamp())
    return jwt.encode(to_encode, secret, algorithm="HS512")


def authenticate_token(email: str, password: str) -> Dict[str, Any]:
    email = email.strip().lower()

    user_db = db.users.find_one({"email": email})
    if not user_db or "password" not in user_db:
        raise HTTPException(status_code=401, detail="Cannot authenticate")

    if not compare_password(password, user_db["password"]):
        raise HTTPException(status_code=401, detail="Cannot authenticate")

    profilna = user_db.get("profilnaSlika")
    role = user_db.get("role")

    secret = os.getenv("JWT_SECRET") or os.getenv("TOKEN_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET/TOKEN_SECRET is not set")

    expires = timedelta(hours=1)

    token = _create_jwt(
        payload={"email": email, "profilna": profilna, "role": role},
        secret=secret,
        expires_in=expires,
    )

    return {
        "token": token,
        "email": email,
        "profilna": profilna,
        "role": role,
    }


async def verify_token(
    credentials: Optional[HTTPAuthorizationCredentials] = None,
) -> Dict[str, Any]:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    token = credentials.credentials

    secret = os.getenv("JWT_SECRET") or os.getenv("TOKEN_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET/TOKEN_SECRET is not set")

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS512"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Mali helper da se verify radi “kao middleware” preko HTTPBearer
async def require_user(
    creds: Optional[HTTPAuthorizationCredentials] = bearer_scheme,
) -> Dict[str, Any]:
    return await verify_token(creds)
