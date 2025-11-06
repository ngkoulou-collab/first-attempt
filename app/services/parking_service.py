"""Domain services for parking availability."""

from __future__ import annotations

import asyncio
import contextlib
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from ..config import settings
from ..providers.base import ParkingDataProvider
from ..providers.mock import MockParkingProvider
from ..providers.remote import RemoteParkingProvider


@dataclass
class ParkingRecord:
    street_name: str
    available_spots: int
    total_spots: int
    coordinates: tuple[float, float]
    last_updated: str
    source: str


class ParkingService:
    """Keep a cached view of parking availability for fast reads."""

    def __init__(self, provider: Optional[ParkingDataProvider] = None) -> None:
        self._provider = provider or self._resolve_provider()
        self._records: Dict[str, ParkingRecord] = {}
        self._lock = asyncio.Lock()
        self._refresh_task: Optional[asyncio.Task] = None

    def _resolve_provider(self) -> ParkingDataProvider:
        if settings.provider == "mock":
            return MockParkingProvider(settings.mock_data_path)
        if settings.provider == "remote":
            if not settings.remote_base_url:
                raise RuntimeError("REMOTE_BASE_URL must be configured for remote provider")
            return RemoteParkingProvider(settings.remote_base_url, settings.api_key)
        raise RuntimeError(f"Unsupported provider '{settings.provider}'")

    async def start(self) -> None:
        if self._refresh_task is None:
            await self.refresh()
            self._refresh_task = asyncio.create_task(self._refresh_loop())

    async def stop(self) -> None:
        if self._refresh_task:
            self._refresh_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._refresh_task
            self._refresh_task = None

    async def _refresh_loop(self) -> None:
        while True:
            await asyncio.sleep(settings.refresh_interval_seconds)
            await self.refresh()

    async def refresh(self) -> None:
        async with self._lock:
            new_records = {}
            async for entry in self._provider.fetch_all():
                record = ParkingRecord(
                    street_name=entry["street_name"],
                    available_spots=int(entry["available_spots"]),
                    total_spots=int(entry["total_spots"]),
                    coordinates=tuple(entry["coordinates"]),
                    last_updated=entry.get("last_updated")
                    or datetime.utcnow().isoformat() + "Z",
                    source=entry.get("source", "unknown"),
                )
                new_records[record.street_name.lower()] = record
            self._records = new_records

    async def get_all(self) -> List[ParkingRecord]:
        async with self._lock:
            return list(self._records.values())

    async def get_by_street(self, street_name: str) -> Optional[ParkingRecord]:
        async with self._lock:
            return self._records.get(street_name.lower())


parking_service = ParkingService()
