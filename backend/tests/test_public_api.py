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
        "store_id": "STORE_1001",
        "campaign_id": "CMP_1001",
        "device_anon_id": "device-abc",
        "message": "Interested in this offer",
    }
    response = await client.post("/v1/public/enquiries", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["enquiry_id"].startswith("ENQ_")
    assert data["status"] == "NEW"
    assert data["created_at"] is not None
    assert set(data.keys()) == {"enquiry_id", "status", "created_at"}


@pytest.mark.asyncio
async def test_post_enquiry_returns_404_for_unknown_store(client):
    payload = {
        "store_id": "STORE_X",
        "campaign_id": "CMP_1001",
        "device_anon_id": "device-abc",
        "message": "Interested in this offer",
    }
    response = await client.post("/v1/public/enquiries", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Store not found"


@pytest.mark.asyncio
async def test_post_enquiry_returns_404_for_unknown_campaign(client):
    payload = {
        "store_id": "STORE_1001",
        "campaign_id": "CMP_X",
        "device_anon_id": "device-abc",
        "message": "Interested in this offer",
    }
    response = await client.post("/v1/public/enquiries", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Campaign not found"


@pytest.mark.asyncio
async def test_post_enquiry_returns_400_for_empty_device_anon_id(client):
    payload = {
        "store_id": "STORE_1001",
        "campaign_id": "CMP_1001",
        "device_anon_id": "   ",
        "message": "Interested in this offer",
    }
    response = await client.post("/v1/public/enquiries", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "device_anon_id must not be empty"
