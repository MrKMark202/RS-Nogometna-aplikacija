from fastapi import APIRouter, Depends, HTTPException
from db import db
from models import Transfer
from utils import verify_token
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/record")
async def record_transfer(transfer: Transfer, user=Depends(verify_token)):
    try:
        transfer_data = transfer.dict()
        transfer_data["korisnikEmail"] = user["email"]
        
        result = db.transfers.insert_one(transfer_data)
        transfer_id = str(result.inserted_id)
        
        # Save contract to 'concrats' collection
        db.concrats.insert_one({
            "igracId": transfer_data["igracId"],
            "klubId": transfer_data["noviKlubId"],
            "vrijednost": transfer_data.get("vrijednost", 0),
            "datum": transfer_data["datumTransfera"],
            "tip": "TRANSFER",
            "izKluba": transfer_data["stariKlubId"],
            "uKlub": transfer_data["noviKlubId"]
        })
        
        # Update current club of the player in footballer-microservice database (shared DB)
        db.footballers.update_one(
            {"_id": ObjectId(transfer_data["igracId"])},
            {"$set": {"klub": transfer_data["noviKlubId"]}}
        )
        
        transfer_data["_id"] = transfer_id
        return transfer_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/povijest", response_model=List[dict])
async def get_transfer_history(igracId: str = None, user=Depends(verify_token)):
    try:
        query = {}
        if igracId:
            query["igracId"] = igracId
            
        transfers = list(db.transfers.find(query))
        for t in transfers:
            t["_id"] = str(t["_id"])
            
        return transfers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contracts/{igracId}")
async def get_player_contracts_db(igracId: str, user=Depends(verify_token)):
    try:
        # Fetching from 'concrats' collection
        contracts = list(db.concrats.find({"igracId": igracId}))
        for c in contracts:
            c["_id"] = str(c["_id"])
        return contracts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
