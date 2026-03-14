from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.assets import router as assets_router
from app.routers.audit import router as audit_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(assets_router)
app.include_router(audit_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
