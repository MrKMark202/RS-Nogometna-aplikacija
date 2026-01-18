from db import db
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId

router = APIRouter(tags=["league"])


# ---------- Helpers ----------
def oid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Neispravan ID")


def serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "korisnik" in doc and isinstance(doc["korisnik"], ObjectId):
        doc["korisnik"] = str(doc["korisnik"])
    return doc

# ---------- Request modeli ----------
class CreateLeagueRequest(BaseModel):
    naziv: str = Field(min_length=2, max_length=100)
    godinaOsnivanja: str = Field(min_length=4, max_length=10)
    drzava: str = Field(min_length=2, max_length=60)
    grbLige: str = Field(min_length=1)
    korisnikEmail: EmailStr


class DeleteLeagueRequest(BaseModel):
    leagueId: str
    korisnikEmail: EmailStr
    
    
# --- Rute ---

@router.get("/dohvat")
def dohvati_lige(korisnikEmail: EmailStr = Query(...)):
    user = db.users.find_one({"email": str(korisnikEmail).lower().strip()})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    cursor = db.leagues.find({"korisnik": user["_id"]}).sort("naziv", 1)
    return [serialize(doc) for doc in cursor]


@router.post("/create")
def create_league(payload: CreateLeagueRequest):
    user = db.users.find_one({"email": str(payload.korisnikEmail).lower().strip()})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    # provjera duplikata naziva (friendly poruka)
    exists = db.leagues.find_one({"naziv": payload.naziv})
    if exists:
        raise HTTPException(status_code=409, detail="Liga s tim nazivom već postoji")

    doc = {
        "naziv": payload.naziv,
        "godinaOsnivanja": payload.godinaOsnivanja,
        "drzava": payload.drzava,
        "grbLige": payload.grbLige,
        "korisnik": user["_id"],
    }

    res = db.leagues.insert_one(doc)
    doc["_id"] = res.inserted_id
    return serialize(doc)


@router.delete("/delete")
def delete_league(payload: DeleteLeagueRequest):
    user = db.users.find_one({"email": str(payload.korisnikEmail).lower().strip()})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    league_id = oid(payload.leagueId)

    league = db.leagues.find_one({"_id": league_id})
    if not league:
        raise HTTPException(status_code=404, detail="Liga nije pronađena")

    if league.get("korisnik") != user["_id"]:
        raise HTTPException(status_code=403, detail="Nemaš pravo obrisati ovu ligu")

    db.leagues.delete_one({"_id": league_id})
    return {"result": True}