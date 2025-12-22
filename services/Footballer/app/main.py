from fastapi import FastAPI

app = FastAPI(title="footballer-service")

@app.get("/health")
def health():
    return {"service": "footballer", "status": "ok"}
