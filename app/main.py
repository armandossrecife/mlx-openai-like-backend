from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.chats import router as chats_router
from app.routers.inference import router as inference_router
from app.routers.health import router as health_router

app = FastAPI(title="MLX Backend (Auth + Chats)", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOW_ORIGINS],  # "*" em dev; restrinja em prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(inference_router)
app.include_router(health_router)