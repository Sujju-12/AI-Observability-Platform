from fastapi import FastAPI

from app.core.database import get_db_connection
from app.core.logging_config import logger
from app.models.user import UserCreate
from app.services.user_service import create_user
from app.core.telemetry import setup_telemetry
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Auth Service",
    description="Authentication microservice for AI Observability Platform",
    version="0.1.2"
)

setup_telemetry(app)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "Auth Service Running"
    }


@app.get("/health")
def health_check():
    logger.info("Health check requested")

    try:
        connection = get_db_connection()
        connection.close()

        logger.info("Database connectivity successful")

        return {
            "status": "healthy",
            "service": "auth-service",
            "database": "connected"
        }

    except Exception as error:
        logger.error(f"Health check failed: {error}")

        return {
            "status": "unhealthy",
            "service": "auth-service",
            "database": "disconnected",
            "error": str(error)
        }


@app.post("/users")
def register_user(user: UserCreate):
    logger.info(f"User registration requested: {user.username}")

    return create_user(user.username, user.email)
