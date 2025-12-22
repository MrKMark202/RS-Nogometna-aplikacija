from fastapi import FastAPI

app = FastAPI(title="transfers-service")

@app.get("/health")
def health():
    return {"service": "transfers", "status": "ok"}
