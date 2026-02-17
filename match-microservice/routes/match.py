from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from db import db
from utils import verify_token

router = APIRouter(tags=["match"])


# ---------- Helpers ----------

def _oid(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=422, detail="Neispravan ID")
    return ObjectId(value)


def _serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    doc["liga"] = str(doc["liga"])
    doc["domacin"] = str(doc["domacin"])
    doc["gost"] = str(doc["gost"])
    return doc


# ---------- Request model ----------

class CreateMatchRequest(BaseModel):
    kolo: str
    stadionNaziv: str
    mjestoIgranja: str
    gledateljiBroj: str
    datum: str
    satUpisa: str
    liga: str
    domacin: str
    gost: str
    domacinGol: int = Field(ge=0)
    gostiGol: int = Field(ge=0)


# ---------- ROUTES ----------

@router.post("/create")
def create_match(payload: CreateMatchRequest, user=Depends(verify_token)):
    email = user["email"].lower().strip()

    liga_oid = _oid(payload.liga)
    domacin_oid = _oid(payload.domacin)
    gost_oid = _oid(payload.gost)

    # Provjera da liga pripada korisniku
    liga = db.leagues.find_one({
        "_id": liga_oid,
        "korisnikEmail": email
    })
    if not liga:
        raise HTTPException(status_code=404, detail="Liga nije pronađena")

    # Provjera klubova
    domacin = db.clubs.find_one({
        "_id": domacin_oid,
        "korisnikEmail": email
    })
    gost = db.clubs.find_one({
        "_id": gost_oid,
        "korisnikEmail": email
    })

    if not domacin or not gost:
        raise HTTPException(status_code=404, detail="Klub nije pronađen")

    # ---------- Spremi utakmicu ----------

    match_doc = {
        "kolo": payload.kolo,
        "stadionNaziv": payload.stadionNaziv,
        "mjestoIgranja": payload.mjestoIgranja,
        "gledateljiBroj": payload.gledateljiBroj,
        "datum": payload.datum,
        "satUpisa": payload.satUpisa,
        "liga": liga_oid,
        "domacin": domacin_oid,
        "gost": gost_oid,
        "domacinGol": payload.domacinGol,
        "gostiGol": payload.gostiGol,
        "korisnikEmail": email
    }

    res = db.matches.insert_one(match_doc)
    match_doc["_id"] = res.inserted_id

    # ---------- Izračun bodova ----------

    dom_bod = 0
    gos_bod = 0

    if payload.domacinGol > payload.gostiGol:
        dom_bod = 3
    elif payload.domacinGol < payload.gostiGol:
        gos_bod = 3
    else:
        dom_bod = 1
        gos_bod = 1

    # ---------- Update tablice domaćin ----------

    db.tablica.update_one(
        {
            "liga": liga_oid,
            "klub": domacin_oid,
            "korisnikEmail": email
        },
        {
            "$inc": {
                "bodovi": dom_bod,
                "postignutiPogodci": payload.domacinGol,
                "primljeniPogodci": payload.gostiGol,
                "odigranihDvoboja": 1
            }
        }
    )

    # ---------- Update tablice gost ----------

    db.tablica.update_one(
        {
            "liga": liga_oid,
            "klub": gost_oid,
            "korisnikEmail": email
        },
        {
            "$inc": {
                "bodovi": gos_bod,
                "postignutiPogodci": payload.gostiGol,
                "primljeniPogodci": payload.domacinGol,
                "odigranihDvoboja": 1
            }
        }
    )

    return _serialize(match_doc)
