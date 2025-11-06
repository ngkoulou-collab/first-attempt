"""API routes for the parking availability service."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..services.parking_service import parking_service

router = APIRouter()


@router.get("/health", summary="Service health check")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/parking", summary="List availability for all known streets")
async def list_parking() -> list[dict]:
    records = await parking_service.get_all()
    return [record.__dict__ for record in records]


@router.get("/parking/{street_name}", summary="Get availability for a specific street")
async def get_parking_for_street(street_name: str) -> dict:
    record = await parking_service.get_by_street(street_name)
    if record is None:
        raise HTTPException(status_code=404, detail=f"No parking data for '{street_name}'")
    return record.__dict__

