from pydantic import BaseModel

from app.schemas.campaign import CampaignResponse
from app.schemas.store import StoreResponse


class StoreCampaignResponse(BaseModel):
    store: StoreResponse
    active_campaign: CampaignResponse | None = None
