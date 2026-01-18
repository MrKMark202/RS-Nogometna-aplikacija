from fastapi import FastAPI

app = FastAPI(title="match-review-service")

@app.get("/health")
def health():
    return {"service": "match-review", "status": "ok"}
