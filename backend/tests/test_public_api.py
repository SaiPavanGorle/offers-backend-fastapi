from datetime import datetime, timezone

import pytest


@pytest.mark.asyncio
async def test_get_store_by_ibeacon_returns_store_and_campaign(client):
    response = await client.get(
        "/v1/public/stores/by-ibeacon",
        params={
            "uuid": "F7826DA6-4FA2-4E98-8024-BC5B71E0893E",
            "major": 1001,
            "minor": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["store"]["store_id"] == "STORE_1001"
    assert data["active_campaign"]["campaign_id"] == "CMP_1001"


@pytest.mark.asyncio
async def test_get_active_campaign_by_store_id(client):
    response = await client.get("/v1/public/stores/STORE_1001/active-campaign")
    assert response.status_code == 200
    data = response.json()
    assert data["store"]["store_id"] == "STORE_1001"
    assert data["active_campaign"]["is_active"] is True


@pytest.mark.asyncio
async def test_post_enquiry_creates_record(client):
    payload = {
        "enquiry_id": "ENQ_0001",
        "store_id": "STORE_1001",
        "campaign_id": "CMP_1001",
        "device_anon_id": "device-abc",
        "message": "Interested in this offer",
        "status": "new",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.post("/v1/public/enquiries", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["enquiry_id"] == "ENQ_0001"
    assert data["server_received_at"] is not None
