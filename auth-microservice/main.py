import os
from db import db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from routes.user import router as user_router
from routes.auth import router as auth_router

app = FastAPI(title="auth-service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"service": "auth", "status": "ok"}

@app.on_event("startup")
def startup_db_check():
    if not os.getenv("MONGO_URI"):
        raise RuntimeError("MONGO_URI is not set")

    db.command("ping")
    db.users.create_index("email", unique=True)

    print("auth-service connected to MongoDB")

app.include_router(auth_router, prefix="/api/auth")
app.include_router(user_router, prefix="/api/user")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
