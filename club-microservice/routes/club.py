from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

from db import db
from utils import verify_token

router = APIRouter(tags=["club"])


# ---------- Helpers ----------

def _oid(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=422, detail="Neispravan ID")
    return ObjectId(value)


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    if "liga" in doc and isinstance(doc["liga"], ObjectId):
        doc["liga"] = str(doc["liga"])
    return doc


# ---------- Request modeli ----------

class CreateClubRequest(BaseModel):
    naziv: str
    godinaOsnivanja: str
    drzava: str
    grbKluba: str
    ligaId: str


class DeleteClubRequest(BaseModel):
    clubId: str


# ---------- Routes ----------

@router.get("/health")
def health():
    return {"service": "club", "status": "ok"}

@router.post("/create")
def create_club(payload: CreateClubRequest, user=Depends(verify_token)):
    email = user["email"]

    liga_oid = _oid(payload.ligaId)

    liga = db.leagues.find_one({
        "_id": liga_oid,
        "korisnikEmail": email
    })
    if not liga:
        raise HTTPException(status_code=404, detail="Liga nije pronađena")

    existing = db.clubs.find_one({
        "naziv": payload.naziv,
        "korisnikEmail": email
    })
    if existing:
        raise HTTPException(status_code=409, detail="Klub s tim nazivom već postoji")

    doc = {
        "naziv": payload.naziv,
        "godinaOsnivanja": payload.godinaOsnivanja,
        "drzava": payload.drzava,
        "grbKluba": payload.grbKluba,
        "liga": liga_oid,
        "korisnikEmail": email,
    }

    res = db.clubs.insert_one(doc)
    klub_id = res.inserted_id

    db.tablica.insert_one({
        "liga": liga_oid,
        "klub": klub_id,
        "korisnikEmail": email,
        "bodovi": 0,
        "postignutiPogodci": 0,
        "primljeniPogodci": 0,
        "odigranihDvoboja": 0
    })

    created = db.clubs.find_one({"_id": klub_id})
    return _serialize(created)


@router.get("/dohvat")
def get_clubs(ligaId: Optional[str] = None, user=Depends(verify_token)):
    email = user["email"]

    q = {"korisnikEmail": email}
    if ligaId:
        q["liga"] = _oid(ligaId)

    cursor = db.clubs.find(q).sort("naziv", 1)
    return [_serialize(c) for c in cursor]


@router.delete("/delete")
def delete_club(payload: DeleteClubRequest, user=Depends(verify_token)):
    email = user["email"]

    club_oid = _oid(payload.clubId)

    club = db.clubs.find_one({"_id": club_oid})
    if not club:
        raise HTTPException(status_code=404, detail="Klub nije pronađen")

    if club.get("korisnikEmail") != email:
        raise HTTPException(status_code=403, detail="Nemaš pravo brisati ovaj klub")

    db.clubs.delete_one({"_id": club_oid})
    return {"result": True}
