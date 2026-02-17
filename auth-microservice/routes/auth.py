from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from db import db
from utils import password_hash, authenticate_token, require_user

router = APIRouter(tags=["auth"])


class SignupRequest(BaseModel):
    ime: str = Field(min_length=1)
    prezime: str = Field(min_length=1)
    datumRodenja: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    profilnaSlika: str = Field(min_length=1)
    pin: int = Field(ge=0, le=99999)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(payload: SignupRequest):
    if db.users.find_one({"email": payload.email}):
        raise HTTPException(status_code=409, detail="Email already exists")

    doc = payload.model_dump()
    doc["email"] = doc["email"].strip().lower()
    doc["password"] = password_hash(doc["password"])

    res = db.users.insert_one(doc)

    return {"result": True, "user_id": str(res.inserted_id)}


@router.post("/login")
def login(payload: LoginRequest):
    return authenticate_token(payload.email, payload.password)


@router.get("/me")
def me(user=Depends(require_user)):
    return {"user": user}
