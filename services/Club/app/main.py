from fastapi import FastAPI

app = FastAPI(title="club-service")

@app.get("/health")
def health():
    return {"service": "club", "status": "ok"}
