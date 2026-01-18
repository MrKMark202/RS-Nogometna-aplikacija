from fastapi import FastAPI

app = FastAPI(title="table-service")

@app.get("/health")
def health():
    return {"service": "table", "status": "ok"}
