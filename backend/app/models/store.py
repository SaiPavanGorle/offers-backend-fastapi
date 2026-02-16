from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Store(Base):
    __tablename__ = "stores"

    store_id: Mapped[str] = mapped_column(String(64), primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    beacon_uuid: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    major: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    minor: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    website_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    campaigns = relationship("Campaign", back_populates="store", cascade="all, delete-orphan")
    enquiries = relationship("Enquiry", back_populates="store", cascade="all, delete-orphan")
