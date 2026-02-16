from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    enquiry_id: Mapped[str] = mapped_column(String(64), primary_key=True, unique=True)
    store_id: Mapped[str] = mapped_column(ForeignKey("stores.store_id", ondelete="CASCADE"), nullable=False, index=True)
    campaign_id: Mapped[str | None] = mapped_column(
        ForeignKey("campaigns.campaign_id", ondelete="SET NULL"), nullable=True, index=True
    )
    device_anon_id: Mapped[str] = mapped_column(String(128), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    server_received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    store = relationship("Store", back_populates="enquiries")
    campaign = relationship("Campaign", back_populates="enquiries")
