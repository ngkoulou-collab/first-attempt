"""Remote parking data provider that delegates to an HTTP API."""

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Optional

from .base import ParkingDataProvider

if TYPE_CHECKING:
    import httpx


class RemoteParkingProvider(ParkingDataProvider):
    """Fetch parking availability data from an HTTP API."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 10.0,
    ) -> None:
        if not base_url:
            raise ValueError("base_url must be provided for the remote provider")

        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout

    async def fetch_all(self) -> AsyncIterator[dict]:  # type: ignore[override]
        headers = {"Accept": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        import httpx

        async with httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout) as client:
            response = await client.get("/parking", headers=headers)
            response.raise_for_status()
            payload = response.json()

        for entry in payload:
            yield {
                "street_name": entry["street_name"],
                "available_spots": entry["available_spots"],
                "total_spots": entry.get("total_spots", 0),
                "coordinates": tuple(entry.get("coordinates", (0.0, 0.0))),
                "last_updated": entry.get("last_updated"),
                "source": entry.get("source", self._base_url),
            }

