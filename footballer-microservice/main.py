import os
from db import db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routes.footballer import router as footballer_router

app = FastAPI(title="footballer-service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"service": "footballer", "status": "ok"}

@app.on_event("startup")
def startup_db_check():
    if not os.getenv("MONGO_URI"):
        raise RuntimeError("MONGO_URI is not set")

    db.command("ping")
    db.footballers.create_index("klub")
    db.footballers.create_index("korisnikEmail")

    print("footballer-microservice connected to MongoDB")

app.include_router(footballer_router, prefix="/api/footballer")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
