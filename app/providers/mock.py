"""Mock parking data provider backed by a static JSON file."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator

from .base import ParkingDataProvider


class MockParkingProvider(ParkingDataProvider):
    """Returns data from a static JSON file for testing or demos."""

    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path

    async def fetch_all(self) -> AsyncIterator[dict]:  # type: ignore[override]
        loop = asyncio.get_running_loop()
        raw_text = await loop.run_in_executor(None, self._data_path.read_text)
        dataset = json.loads(raw_text)
        timestamp = datetime.now(tz=timezone.utc).isoformat()

        for entry in dataset:
            yield {
                "street_name": entry["street_name"],
                "available_spots": entry["available_spots"],
                "total_spots": entry["total_spots"],
                "coordinates": tuple(entry["coordinates"]),
                "last_updated": timestamp,
                "source": "mock-dataset",
            }

