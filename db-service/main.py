from dotenv import load_dotenv
from fastapi import FastAPI
from db import db

load_dotenv()

app = FastAPI(title="DB microservice")

@app.on_event("startup")
def startup_db_check():
    db.command("ping")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/mongo-check")
def mongo_check():
    res = db.ping.insert_one({"ok": True})
    return {"mongo": "ok", "inserted_id": str(res.inserted_id)}