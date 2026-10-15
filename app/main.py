from fastapi import FastAPI

from app.api.incidents import router as incidents_router

app = FastAPI(
    title="Enterprise Incident Intelligence",
    version="0.1.0"
)
app.include_router(incidents_router, prefix="/incidents", tags=["incidents"])

@app.get("/health")
def health():
    return {"status": "healthy"}