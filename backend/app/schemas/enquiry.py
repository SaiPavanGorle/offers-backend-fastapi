from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

EnquiryStatus = Literal["NEW"]


class EnquiryCreate(BaseModel):
    store_id: str = Field(min_length=1, examples=["STORE_1001"])
    campaign_id: str = Field(min_length=1, examples=["CMP_1001"])
    device_anon_id: str = Field(examples=["android-0f4d3e2a"])
    message: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
        examples=["Hi, is this offer still valid today?"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "store_id": "STORE_1001",
                "campaign_id": "CMP_1001",
                "device_anon_id": "android-0f4d3e2a",
                "message": "Can I redeem this offer tomorrow?",
            }
        }
    }


class EnquiryResponse(BaseModel):
    enquiry_id: str
    status: EnquiryStatus
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "enquiry_id": "ENQ_f0ed5a72d3bc4d31",
                "status": "NEW",
                "created_at": "2026-01-15T10:45:31.208095Z",
            }
        },
    }
