"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes import router
from .services.parking_service import parking_service


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover - exercised in integration
    await parking_service.start()
    try:
        yield
    finally:
        await parking_service.stop()


app = FastAPI(
    title="Corfu Real-Time Parking API",
    description=(
        "Provides a unified API for accessing real-time parking availability for "
        "streets in Corfu town, Greece."
    ),
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(router)


@app.get("/", summary="API landing endpoint")
async def index() -> dict[str, str]:
    return {
        "message": "Welcome to the Corfu parking availability API.",
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
