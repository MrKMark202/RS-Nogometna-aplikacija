from fastapi import APIRouter, Depends, HTTPException
from db import db
from models import Footballer
from utils import verify_token
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/create")
async def create_footballer(footballer: Footballer, user=Depends(verify_token)):
    try:
        footballer_data = footballer.dict()
        footballer_data["korisnikEmail"] = user["email"]
        
        result = db.footballers.insert_one(footballer_data)
        footballer_id = str(result.inserted_id)
        
        # Save initial contract to 'concrats' collection
        from datetime import datetime
        db.concrats.insert_one({
            "igracId": footballer_id,
            "klubId": footballer_data["klub"],
            "vrijednost": footballer_data.get("initialValue", 0),
            "datum": datetime.now().strftime("%Y-%m-%d"),
            "tip": "INITIAL_SIGNING",
            "izKluba": "INITIAL_SIGNING",
            "uKlub": footballer_data["klub"],
            "ugovorTrajeDo": footballer_data.get("ugovorTrajeDo") or ""
        })
        
        footballer_data["_id"] = footballer_id
        return footballer_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dohvat", response_model=List[dict])
async def get_footballers(klubId: str = None, user=Depends(verify_token)):
    try:
        query = {}
        if klubId:
            query["klub"] = klubId
            
        footballers = list(db.footballers.find(query))
        for f in footballers:
            f["_id"] = str(f["_id"])
            
        return footballers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{igracId}")
async def delete_footballer(igracId: str, user=Depends(verify_token)):
    try:
        # 1. Delete player
        db.footballers.delete_one({"_id": ObjectId(igracId)})
        
        # 2. Delete all contracts (from 'concrats' collection)
        db.concrats.delete_many({"igracId": igracId})
        
        # 3. Delete all transfers
        db.transfers.delete_many({"igracId": igracId})
        
        return {"message": "Igrač i svi povezani podaci su uspješno izbrisani."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
