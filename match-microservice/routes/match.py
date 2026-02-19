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
    
class DeleteMatchRequest(BaseModel):
    liga: str
    domacin: str
    gost: str
    kolo: str


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

    db.tables.update_one(
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

    db.tables.update_one(
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

@router.get("/dohvat")
def get_matches(ligaId: str, user=Depends(verify_token)):

    email = user["email"]
    liga_oid = _oid(ligaId)

    # --- utakmice ---
    matches = list(db.matches.find({
        "liga": liga_oid,
        "korisnikEmail": email
    }))

    if not matches:
        return []

    # --- svi klubovi iz te lige (JEDAN QUERY) ---
    clubs = list(db.clubs.find({
        "liga": liga_oid,
        "korisnikEmail": email
    }))

    # mapa: id -> naziv
    club_map = {
        str(c["_id"]): c["naziv"]
        for c in clubs
    }
    
    liga = db.leagues.find_one({"_id": liga_oid})
    liga_naziv = liga["naziv"] if liga else ""

    rezultat = []

    for m in matches:
        rezultat.append({
            "kolo": m["kolo"],
            "domacin": club_map.get(str(m["domacin"]), ""),
            "domacinGol": m["domacinGol"],
            "gostiGol": m["gostiGol"],
            "gost": club_map.get(str(m["gost"]), ""),
            "ligaNaziv": liga_naziv,
            "mjesto": m["mjestoIgranja"],
            "stadion": m["stadionNaziv"],
            "gledatelji": m["gledateljiBroj"],
            "datum": m["datum"]
        })
        
    return rezultat

@router.patch("/delete")
def delete_match(request: DeleteMatchRequest):

    liga_oid = ObjectId(request.liga)
    domacin_oid = ObjectId(request.domacin)
    gost_oid = ObjectId(request.gost)

    match = db.matches.find_one({
        "liga": liga_oid,
        "domacin": domacin_oid,
        "gost": gost_oid,
        "kolo": request.kolo
    })

    if not match:
        return {"deleted": 0}

    # ----- BODOVI -----
    dom_bod = 0
    gos_bod = 0

    if match["domacinGol"] > match["gostiGol"]:
        dom_bod = -3
    elif match["domacinGol"] < match["gostiGol"]:
        gos_bod = -3
    else:
        dom_bod = -1
        gos_bod = -1

    # ----- UPDATE DOMACIN -----
    db.tables.update_one(
        {"liga": liga_oid, "klub": domacin_oid},
        {
            "$inc": {
                "bodovi": dom_bod,
                "postignutiPogodci": -match["domacinGol"],
                "primljeniPogodci": -match["gostiGol"],
                "odigranihDvoboja": -1
            }
        }
    )

    # ----- UPDATE GOST -----
    db.tables.update_one(
        {"liga": liga_oid, "klub": gost_oid},
        {
            "$inc": {
                "bodovi": gos_bod,
                "postignutiPogodci": -match["gostiGol"],
                "primljeniPogodci": -match["domacinGol"],
                "odigranihDvoboja": -1
            }
        }
    )

    # ----- DELETE MATCH -----
    db.matches.delete_one({"_id": match["_id"]})

    return {"deleted": 1}



@router.get("/one")
def get_single_match(liga: str, domacin: str, gost: str, kolo: str):

    match = db.matches.find_one({
        "liga": ObjectId(liga),
        "domacin": ObjectId(domacin),
        "gost": ObjectId(gost),
        "kolo": kolo
    })

    if not match:
        return None

    match["_id"] = str(match["_id"])
    match["liga"] = str(match["liga"])
    match["domacin"] = str(match["domacin"])
    match["gost"] = str(match["gost"])

    return match

