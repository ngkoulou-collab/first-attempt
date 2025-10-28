# Corfu Real-Time Parking API

This project provides a FastAPI application that aggregates real-time parking availability for streets in Corfu town, Greece. It is designed to plug into real data providers when they become available while still offering a mock dataset for local development and demos.

## Features

- FastAPI-powered REST interface with automatic OpenAPI documentation.
- Background refresh loop keeps parking data up-to-date.
- Pluggable provider architecture supporting both mock data and remote HTTP APIs.
- Ready-to-run Docker-free setup with `uvicorn`.
- Example dataset for common streets in Corfu town.

## Getting Started

### Prerequisites

- Python 3.11+
- (Optional) A virtual environment is recommended.

### Installation

```bash
pip install -r requirements.txt
```

### Running the API

```bash
uvicorn app.main:app --reload
```

The service exposes:

- `GET /` – Welcome endpoint with pointers to docs.
- `GET /docs` – Interactive Swagger UI.
- `GET /parking` – List all available streets with current parking availability.
- `GET /parking/{street_name}` – Query availability for a specific street.

### Configuration

Environment variables (or a `.env` file) control the runtime:

| Variable | Default | Description |
| --- | --- | --- |
| `PARKING_PROVIDER` | `mock` | Provider to use: `mock` or `remote`. |
| `MOCK_DATA_PATH` | `data/corfu_parking_sample.json` | Path to the mock dataset. |
| `REMOTE_BASE_URL` | – | Base URL for the remote provider. |
| `REMOTE_API_KEY` | – | Optional Bearer token for the remote provider. |
| `REFRESH_INTERVAL_SECONDS` | `30` | Background refresh cadence. |

When using the `remote` provider, ensure the upstream API exposes a `/parking` endpoint returning JSON in the following format:

```json
[
  {
    "street_name": "Nikiforou Theotoki",
    "available_spots": 12,
    "total_spots": 20,
    "coordinates": [39.6245, 19.9224],
    "last_updated": "2024-02-29T10:30:00Z",
    "source": "corfu-open-data"
  }
]
```

### Testing

Install the development dependencies and run the test suite:

```bash
pip install -r requirements.txt
pytest
```

### Extending the App

- Implement new providers in `app/providers/` by subclassing the `ParkingDataProvider` protocol.
- Add WebSocket routes or push notifications by leveraging FastAPI's WebSocket support.
- Integrate with mapping libraries or front-end dashboards to visualize availability in real time.

## Limitations

Real-time street-level parking availability data for Corfu is not publicly available at the time of writing. The mock dataset simulates plausible values; connect the app to an official or crowdsourced data provider to deliver true live insights.
