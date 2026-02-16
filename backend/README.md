# Proximity Offers Backend (FastAPI MVP)

Production-ready MVP backend for proximity offers using FastAPI + PostgreSQL + SQLAlchemy async + Alembic.

## Stack
- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0 async
- Alembic
- Docker / Docker Compose

## Run with Docker
```bash
cd backend
docker compose up --build
```

API will be available at: `http://localhost:8000`

The container startup command runs:
1. `alembic upgrade head`
2. seed script (`STORE_1001` + active campaign)
3. uvicorn server

## Local run (without Docker)
```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='postgresql+asyncpg://postgres:postgres@localhost:5432/offers_db'
alembic upgrade head
python -m app.run_seed
uvicorn app.main:app --reload
```

## Alembic
Create/update migration manually in `alembic/versions/` then run:
```bash
alembic upgrade head
```

## Public Endpoints
### 1) Get store by iBeacon
```bash
curl "http://localhost:8000/v1/public/stores/by-ibeacon?uuid=F7826DA6-4FA2-4E98-8024-BC5B71E0893E&major=1001&minor=1"
```

### 2) Get active campaign by store id
```bash
curl "http://localhost:8000/v1/public/stores/STORE_1001/active-campaign"
```

### 3) Create enquiry
```bash
curl -X POST "http://localhost:8000/v1/public/enquiries" \
  -H "Content-Type: application/json" \
  -d '{
    "enquiry_id": "ENQ_2001",
    "store_id": "STORE_1001",
    "campaign_id": "CMP_1001",
    "device_anon_id": "device-123",
    "message": "Need more details",
    "status": "new",
    "created_at": "2026-01-01T00:00:00Z"
  }'
```

## Tests
```bash
cd backend
pytest -q
```
