from datetime import timedelta

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.campaign import Campaign
from app.models.store import Store
from app.services.public_service import now_utc


async def seed_data() -> None:
    async with AsyncSessionLocal() as db:
        store = await db.get(Store, "STORE_1001")
        if not store:
            store = Store(
                store_id="STORE_1001",
                name="Demo Beacon Store",
                beacon_uuid="F7826DA6-4FA2-4E98-8024-BC5B71E0893E",
                major=1001,
                minor=1,
                website_url="https://example-store.com",
            )
            db.add(store)

        campaign_exists = await db.scalar(select(Campaign).where(Campaign.campaign_id == "CMP_1001"))
        if not campaign_exists:
            start_at = now_utc()
            campaign = Campaign(
                campaign_id="CMP_1001",
                store_id="STORE_1001",
                title="Welcome Offer",
                description="Get 20% off on featured products this month.",
                banner_url="https://picsum.photos/seed/offers/1200/400",
                start_at=start_at,
                end_at=start_at + timedelta(days=30),
                website_url="https://example-store.com/offers",
                is_active=True,
            )
            db.add(campaign)

        await db.commit()
