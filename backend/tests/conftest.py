from collections.abc import AsyncGenerator
from datetime import timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.db import Base, get_db
from app.main import app
from app.models.campaign import Campaign
from app.models.store import Store
from app.services.public_service import now_utc

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    test_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session() as session:
        store = Store(
            store_id="STORE_1001",
            name="Demo Beacon Store",
            beacon_uuid="F7826DA6-4FA2-4E98-8024-BC5B71E0893E",
            major=1001,
            minor=1,
            website_url="https://example-store.com",
        )
        start_at = now_utc()
        campaign = Campaign(
            campaign_id="CMP_1001",
            store_id="STORE_1001",
            title="Welcome Offer",
            description="Get 20% off",
            banner_url="https://example.com/banner.png",
            start_at=start_at,
            end_at=start_at + timedelta(days=30),
            website_url="https://example-store.com/offers",
            is_active=True,
        )
        session.add_all([store, campaign])
        await session.commit()

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with test_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()
    await engine.dispose()
