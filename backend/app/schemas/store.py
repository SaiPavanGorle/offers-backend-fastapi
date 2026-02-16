from pydantic import BaseModel


class StoreBase(BaseModel):
    store_id: str
    name: str
    beacon_uuid: str
    major: int
    minor: int
    website_url: str | None = None


class StoreResponse(StoreBase):
    model_config = {"from_attributes": True}
