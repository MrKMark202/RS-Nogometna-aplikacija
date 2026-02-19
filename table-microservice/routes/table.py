from db import db
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from utils import verify_token

router = APIRouter(tags=["table"])


def _oid(value: str):
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=422, detail="Neispravan ID")
    return ObjectId(value)


@router.get("/dohvat")
def get_table(ligaId: str, user=Depends(verify_token)):

    email = user["email"]
    liga_oid = _oid(ligaId)

    table_docs = list(db.tables.find({
        "liga": liga_oid,
        "korisnikEmail": email
    }))

    if not table_docs:
        return []

    result = []

    for t in table_docs:
        result.append({
            "klub": t["nazivKluba"],
            "grbKlub": t["grbKlub"],
            "odigranihDvoboja": t["odigranihDvoboja"],
            "postignutiPogodci": t["postignutiPogodci"],
            "primljeniPogodci": t["primljeniPogodci"],
            "bodovi": t["bodovi"]
        })

    return result


@router.get("/dohvat/klub")
def get_single_table(
    ligaId: str,
    klubId: str,
    user=Depends(verify_token)
):
    email = user["email"]

    table = db.tables.find_one({
        "liga": ObjectId(ligaId),
        "klub": ObjectId(klubId),
        "korisnikEmail": email
    })

    if not table:
        return {}

    table["_id"] = str(table["_id"])
    table["liga"] = str(table["liga"])
    table["klub"] = str(table["klub"])

    return table
