from db import db
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from bson import ObjectId
from utils import verify_token
from models import League

router = APIRouter(tags=["league"])


# ---------- Helpers ----------

def oid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Neispravan ID")


def serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc


# ---------- Request modeli (DTO) ----------

class CreateLeagueRequest(BaseModel):
    naziv: str = Field(min_length=2, max_length=100)
    godinaOsnivanja: str = Field(min_length=4, max_length=10)
    drzava: str = Field(min_length=2, max_length=60)
    grbLige: str = Field(min_length=1)


class DeleteLeagueRequest(BaseModel):
    leagueId: str


# ---------- Rute ----------

@router.get("/dohvat")
def dohvati_lige(user=Depends(verify_token)):
    email = user["email"].lower().strip()

    cursor = db.leagues.find(
        {"korisnikEmail": email},
        {"naziv": 1, "grbLige": 1}
    ).sort("naziv", 1)

    return [
        {
            "_id": str(l["_id"]),
            "naziv": l["naziv"],
            "grbLige": l.get("grbLige")
        }
        for l in cursor
    ]

@router.post("/create")
def create_league(payload: CreateLeagueRequest, user=Depends(verify_token)):
    email = user["email"]

    exists = db.leagues.find_one({
        "naziv": payload.naziv,
        "korisnikEmail": email
    })

    if exists:
        raise HTTPException(status_code=409, detail="Liga s tim nazivom već postoji")

    doc = {
        "naziv": payload.naziv,
        "godinaOsnivanja": payload.godinaOsnivanja,
        "drzava": payload.drzava,
        "grbLige": payload.grbLige,
        "korisnikEmail": email,
    }

    res = db.leagues.insert_one(doc)
    doc["_id"] = res.inserted_id

    return serialize(doc)

@router.delete("/delete")
def delete_league(payload: DeleteLeagueRequest, user=Depends(verify_token)):
    email = user["email"].lower().strip()
    league_oid = oid(payload.leagueId)

    league = db.leagues.find_one({
        "_id": league_oid,
        "korisnikEmail": email
    })

    if not league:
        raise HTTPException(status_code=404, detail="Liga nije pronađena")

    # pronađi sve klubove te lige
    club_ids = [
        c["_id"] for c in db.clubs.find(
            {"liga": league_oid, "korisnikEmail": email},
            {"_id": 1}
        )
    ]

    print("CLUB IDS:", club_ids)

    # obriši tablice tih klubova
    db.tables.delete_many({
        "klub": {"$in": club_ids},
        "korisnikEmail": email
    })

    # obriši klubove
    db.clubs.delete_many({
        "liga": league_oid,
        "korisnikEmail": email
    })

    # obriši ligu
    db.leagues.delete_one({"_id": league_oid})

    return {"result": True}
