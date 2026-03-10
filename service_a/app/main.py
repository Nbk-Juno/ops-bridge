from fastapi import FastAPI
from app.database import Base, engine
from app.routers.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
