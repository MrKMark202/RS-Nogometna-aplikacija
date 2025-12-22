from fastapi import FastAPI

app = FastAPI(title="match-service")

@app.get("/health")
def health():
    return {"service": "match", "status": "ok"}
