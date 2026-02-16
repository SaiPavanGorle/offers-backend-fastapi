from datetime import datetime

from pydantic import BaseModel


class CampaignBase(BaseModel):
    campaign_id: str
    store_id: str
    title: str
    description: str
    banner_url: str | None = None
    start_at: datetime
    end_at: datetime
    website_url: str | None = None
    is_active: bool


class CampaignResponse(CampaignBase):
    model_config = {"from_attributes": True}
