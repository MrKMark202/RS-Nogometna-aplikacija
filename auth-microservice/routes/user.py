from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from db import db
from utils import password_hash

router = APIRouter(tags=["user"])


# --- Request modeli ---

class DeleteUserRequest(BaseModel):
    userEmail: EmailStr


class UpdateProfilnaRequest(BaseModel):
    email: EmailStr
    profilna: str = Field(min_length=1)


class UpdatePasswordRequest(BaseModel):
    email: EmailStr
    lozinka: str = Field(min_length=6, max_length=72)
    pin: int = Field(ge=0, le=99999) 


# --- Rute ---

@router.get("/dohvat")
def dohvati_korisnika(email: EmailStr = Query(...)):
    user_db = db.users.find_one({"email": str(email)})
    if not user_db:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    user_db.pop("password", None)
    user_db["_id"] = str(user_db["_id"])
    return user_db


@router.patch("/delete")
def delete_user(payload: DeleteUserRequest):
    user = db.users.find_one({"email": payload.userEmail})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    user_id = user["_id"]  # ObjectId

    # delete user
    db.users.delete_many({"_id": user_id})

    # delete related docs
    db.leagues.delete_many({"korisnik": user_id})
    db.clubs.delete_many({"korisnik": user_id})
    db.matches.delete_many({"korisnik": user_id})
    db.tables.delete_many({"korisnik": user_id})

    return {"result": True}


@router.patch("/update/podaci")
def update_podaci(payload: UpdateProfilnaRequest):
    res = db.users.update_one(
        {"email": payload.email},
        {"$set": {"profilnaSlika": payload.profilna}},
    )

    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    return {"result": True}


@router.patch("/update/lozinka")
def update_lozinka(payload: UpdatePasswordRequest):
    user_db = db.users.find_one({"email": payload.email.strip().lower()})
    if not user_db:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")
    
    if int(user_db.get("pin", -1)) != payload.pin:
        raise HTTPException(status_code=401, detail="Neispravan PIN")

    hashed = password_hash(payload.lozinka)

    db.users.update_one(
        {"_id": user_db["_id"]},
        {"$set": {"password": hashed}},
    )

    return {"result": True}
