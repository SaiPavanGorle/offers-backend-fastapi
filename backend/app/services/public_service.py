from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.models.enquiry import Enquiry
from app.models.store import Store
from app.schemas.enquiry import EnquiryCreate


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


async def get_store_by_ibeacon(db: AsyncSession, uuid: str, major: int, minor: int) -> Store | None:
    stmt = select(Store).where(
        and_(Store.beacon_uuid == uuid, Store.major == major, Store.minor == minor)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_active_campaign_for_store(db: AsyncSession, store_id: str) -> Campaign | None:
    current_time = now_utc()
    stmt = (
        select(Campaign)
        .where(
            and_(
                Campaign.store_id == store_id,
                Campaign.is_active.is_(True),
                Campaign.start_at <= current_time,
                Campaign.end_at >= current_time,
            )
        )
        .order_by(Campaign.start_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_enquiry(db: AsyncSession, payload: EnquiryCreate) -> Enquiry:
    created_at = now_utc()
    enquiry = Enquiry(
        enquiry_id=f"ENQ_{uuid4().hex[:16]}",
        store_id=payload.store_id,
        campaign_id=payload.campaign_id,
        device_anon_id=payload.device_anon_id,
        message=payload.message or "",
        status="NEW",
        created_at=created_at,
        server_received_at=created_at,
    )
    db.add(enquiry)
    await db.commit()
    await db.refresh(enquiry)
    return enquiry
