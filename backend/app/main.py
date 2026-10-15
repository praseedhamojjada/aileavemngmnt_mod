
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from . import models
from .database import Base, engine
from .routers.auth import router as auth_router
from .routers.leaves import router as leaves_router
from .routers.dashboard import router as dashboard_router
from .routers.ai import router as ai_router
from .routers.attendance import router as attendance_router
from .routers.notifications import router as notifications_router


# Create tables from the registered SQLAlchemy models.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CampusLeave AI",
    description="AI-powered College Leave Management System",
    version="1.0.0",
)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_url = os.getenv("FRONTEND_URL", "").strip()
if frontend_url:
    allowed_origins.extend(
        origin.strip()
        for origin in frontend_url.split(",")
        if origin.strip()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(leaves_router)
app.include_router(attendance_router)
app.include_router(notifications_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CampusLeave AI",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "status": "healthy",
        }
    except Exception:
        return {
            "database": "disconnected",
            "status": "unhealthy",
        }
