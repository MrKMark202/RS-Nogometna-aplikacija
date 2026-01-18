from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

from db import db
from bson import ObjectId


router = APIRouter(tags=["club"])


# ---------- Helpers ----------

def _oid(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=422, detail="Neispravan ID")
    return ObjectId(value)


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    # pretvori reference ako postoje
    if "liga" in doc and isinstance(doc["liga"], ObjectId):
        doc["liga"] = str(doc["liga"])
    if "korisnik" in doc and isinstance(doc["korisnik"], ObjectId):
        doc["korisnik"] = str(doc["korisnik"])
    return doc


# ---------- Request modeli ----------

class CreateClubRequest(BaseModel):
    naziv: str = Field(min_length=1)
    godinaOsnivanja: str = Field(min_length=1)
    drzava: str = Field(min_length=1)
    grbKluba: str = Field(min_length=1)
    ligaId: str = Field(min_length=24, max_length=24)
    korisnikEmail: EmailStr


class DeleteClubRequest(BaseModel):
    clubId: str = Field(min_length=24, max_length=24)
    korisnikEmail: EmailStr


# ---------- Routes ----------

@router.get("/health")
def health():
    return {"service": "club", "status": "ok"}


@router.get("/leagues")
def get_leagues_for_select(korisnikEmail: EmailStr = Query(...)):
    """
    Vrati lige za korisnika (da ih koristiš u <select>).
    """
    user = db.users.find_one({"email": str(korisnikEmail)})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    cursor = db.leagues.find({"korisnik": user["_id"]}).sort("naziv", 1)
    leagues = []
    for l in cursor:
        leagues.append({
            "_id": str(l["_id"]),
            "naziv": l.get("naziv"),
            "drzava": l.get("drzava"),
            "grbLige": l.get("grbLige"),
        })
    return leagues


@router.post("/create")
def create_club(payload: CreateClubRequest):
    user = db.users.find_one({"email": str(payload.korisnikEmail)})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    liga_oid = _oid(payload.ligaId)

    liga = db.leagues.find_one({"_id": liga_oid, "korisnik": user["_id"]})
    if not liga:
        raise HTTPException(status_code=404, detail="Liga nije pronađena")

    # unique: naziv kluba po korisniku (da može drugi korisnik imati isti naziv)
    existing = db.clubs.find_one({"naziv": payload.naziv, "korisnik": user["_id"]})
    if existing:
        raise HTTPException(status_code=409, detail="Klub s tim nazivom već postoji")

    doc = {
        "naziv": payload.naziv,
        "godinaOsnivanja": payload.godinaOsnivanja,
        "drzava": payload.drzava,
        "grbKluba": payload.grbKluba,
        "liga": liga_oid,
        "korisnik": user["_id"],
    }

    res = db.clubs.insert_one(doc)
    created = db.clubs.find_one({"_id": res.inserted_id})
    return _serialize(created)


@router.get("/dohvat")
def get_clubs(korisnikEmail: EmailStr = Query(...), ligaId: Optional[str] = None):
    user = db.users.find_one({"email": str(korisnikEmail)})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    q = {"korisnik": user["_id"]}
    if ligaId:
        q["liga"] = _oid(ligaId)

    cursor = db.clubs.find(q).sort("naziv", 1)

    clubs = []
    for c in cursor:
        clubs.append(_serialize(c))
    return clubs


@router.delete("/delete")
def delete_club(payload: DeleteClubRequest):
    user = db.users.find_one({"email": str(payload.korisnikEmail)})
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    club_oid = _oid(payload.clubId)

    club = db.clubs.find_one({"_id": club_oid})
    if not club:
        raise HTTPException(status_code=404, detail="Klub nije pronađen")

    if club.get("korisnik") != user["_id"]:
        raise HTTPException(status_code=403, detail="Nemaš pravo brisati ovaj klub")

    db.clubs.delete_one({"_id": club_oid})
    return {"result": True}