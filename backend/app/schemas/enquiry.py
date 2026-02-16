from datetime import datetime

from pydantic import BaseModel, Field


class EnquiryCreate(BaseModel):
    enquiry_id: str = Field(min_length=3, max_length=64)
    store_id: str
    campaign_id: str | None = None
    device_anon_id: str
    message: str = Field(min_length=1, max_length=2000)
    status: str = "new"
    created_at: datetime


class EnquiryResponse(BaseModel):
    enquiry_id: str
    store_id: str
    campaign_id: str | None = None
    device_anon_id: str
    message: str
    status: str
    created_at: datetime
    server_received_at: datetime

    model_config = {"from_attributes": True}
