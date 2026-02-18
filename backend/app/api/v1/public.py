from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.campaign import Campaign
from app.models.store import Store
from app.schemas.enquiry import EnquiryCreate, EnquiryResponse
from app.schemas.public import StoreCampaignResponse
from app.services.public_service import create_enquiry, get_active_campaign_for_store, get_store_by_ibeacon

router = APIRouter(prefix="/v1/public", tags=["public"])


@router.get("/stores/by-ibeacon", response_model=StoreCampaignResponse)
async def get_store_by_beacon(
    uuid: str = Query(..., description="iBeacon UUID"),
    major: int = Query(...),
    minor: int = Query(...),
    db: AsyncSession = Depends(get_db),
) -> StoreCampaignResponse:
    store = await get_store_by_ibeacon(db, uuid=uuid, major=major, minor=minor)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    active_campaign = await get_active_campaign_for_store(db, store_id=store.store_id)
    return StoreCampaignResponse(store=store, active_campaign=active_campaign)


@router.get("/stores/{store_id}/active-campaign", response_model=StoreCampaignResponse)
async def get_store_active_campaign(store_id: str, db: AsyncSession = Depends(get_db)) -> StoreCampaignResponse:
    store = await db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    active_campaign = await get_active_campaign_for_store(db, store_id=store_id)
    return StoreCampaignResponse(store=store, active_campaign=active_campaign)


@router.post("/enquiries", response_model=EnquiryResponse, status_code=status.HTTP_201_CREATED)
async def post_enquiry(payload: EnquiryCreate, db: AsyncSession = Depends(get_db)) -> EnquiryResponse:
    if not payload.device_anon_id.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="device_anon_id must not be empty")

    store = await db.get(Store, payload.store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    campaign = await db.get(Campaign, payload.campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    try:
        enquiry = await create_enquiry(db, payload)
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid enquiry payload") from exc
    return EnquiryResponse.model_validate(enquiry)
