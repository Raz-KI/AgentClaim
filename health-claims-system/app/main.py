from fastapi import FastAPI
from app.api.claims import router as claims_router

app = FastAPI()

app.include_router(claims_router)