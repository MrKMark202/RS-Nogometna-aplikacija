from fastapi import FastAPI

app = FastAPI(title="league-service")

@app.get("/health")
def health():
    return {"service": "league", "status": "ok"}
