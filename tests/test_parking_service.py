from __future__ import annotations

from pathlib import Path

import asyncio
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from app.providers.mock import MockParkingProvider
from app.services.parking_service import ParkingService


def test_refresh_loads_mock_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data_path = tmp_path / "data.json"
    data_path.write_text(
        """
        [
            {
                \"street_name\": \"Nikiforou Theotoki\",
                \"available_spots\": 10,
                \"total_spots\": 20,
                \"coordinates\": [39.0, 19.0]
            }
        ]
        """
    )

    service = ParkingService(provider=MockParkingProvider(data_path))
    asyncio.run(service.refresh())

    record = asyncio.run(service.get_by_street("Nikiforou Theotoki"))
    assert record is not None
    assert record.street_name == "Nikiforou Theotoki"
    assert record.available_spots == 10
    assert record.total_spots == 20
    assert record.coordinates == (39.0, 19.0)


@pytest.mark.parametrize("street_name,expected", [
    ("Nikiforou Theotoki", True),
    ("Nonexistent", False),
])
def test_get_by_street(tmp_path: Path, street_name: str, expected: bool) -> None:
    data_path = tmp_path / "data.json"
    data_path.write_text(
        """
        [
            {
                \"street_name\": \"Nikiforou Theotoki\",
                \"available_spots\": 5,
                \"total_spots\": 12,
                \"coordinates\": [39.0, 19.0]
            }
        ]
        """
    )

    service = ParkingService(provider=MockParkingProvider(data_path))
    asyncio.run(service.refresh())
    record = asyncio.run(service.get_by_street(street_name))

    assert (record is not None) is expected
