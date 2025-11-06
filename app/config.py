"""Application configuration utilities."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional


_DEF_ENV_PATH = Path(".env")


def _load_dotenv(path: Path = _DEF_ENV_PATH) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


@dataclass
class Settings:
    """Runtime configuration loaded from environment variables."""

    provider: str = os.getenv("PARKING_PROVIDER", "mock")
    mock_data_path: Path = Path(os.getenv("MOCK_DATA_PATH", "data/corfu_parking_sample.json"))
    remote_base_url: Optional[str] = os.getenv("REMOTE_BASE_URL")
    api_key: Optional[str] = os.getenv("REMOTE_API_KEY")
    refresh_interval_seconds: int = int(os.getenv("REFRESH_INTERVAL_SECONDS", "30"))


settings = Settings()
