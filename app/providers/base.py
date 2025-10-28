"""Interfaces for parking data providers."""

from __future__ import annotations

from typing import AsyncIterator, Protocol


class ParkingObservation(Protocol):
    street_name: str
    available_spots: int
    total_spots: int
    coordinates: tuple[float, float]
    last_updated: str
    source: str


class ParkingDataProvider(Protocol):
    """A provider capable of fetching current parking availability data."""

    async def fetch_all(self) -> AsyncIterator[ParkingObservation]:
        """Return an async iterator of parking observations."""

