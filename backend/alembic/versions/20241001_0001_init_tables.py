"""initial tables

Revision ID: 20241001_0001
Revises: 
Create Date: 2024-10-01 00:00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20241001_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stores",
        sa.Column("store_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("beacon_uuid", sa.String(length=64), nullable=False),
        sa.Column("major", sa.Integer(), nullable=False),
        sa.Column("minor", sa.Integer(), nullable=False),
        sa.Column("website_url", sa.String(length=512), nullable=True),
        sa.PrimaryKeyConstraint("store_id"),
        sa.UniqueConstraint("store_id"),
    )
    op.create_index(op.f("ix_stores_beacon_uuid"), "stores", ["beacon_uuid"], unique=False)
    op.create_index(op.f("ix_stores_major"), "stores", ["major"], unique=False)
    op.create_index(op.f("ix_stores_minor"), "stores", ["minor"], unique=False)

    op.create_table(
        "campaigns",
        sa.Column("campaign_id", sa.String(length=64), nullable=False),
        sa.Column("store_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("banner_url", sa.String(length=512), nullable=True),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("website_url", sa.String(length=512), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["store_id"], ["stores.store_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("campaign_id"),
        sa.UniqueConstraint("campaign_id"),
    )
    op.create_index(op.f("ix_campaigns_end_at"), "campaigns", ["end_at"], unique=False)
    op.create_index(op.f("ix_campaigns_is_active"), "campaigns", ["is_active"], unique=False)
    op.create_index(op.f("ix_campaigns_start_at"), "campaigns", ["start_at"], unique=False)
    op.create_index(op.f("ix_campaigns_store_id"), "campaigns", ["store_id"], unique=False)

    op.create_table(
        "enquiries",
        sa.Column("enquiry_id", sa.String(length=64), nullable=False),
        sa.Column("store_id", sa.String(length=64), nullable=False),
        sa.Column("campaign_id", sa.String(length=64), nullable=True),
        sa.Column("device_anon_id", sa.String(length=128), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("server_received_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.campaign_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["store_id"], ["stores.store_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("enquiry_id"),
        sa.UniqueConstraint("enquiry_id"),
    )
    op.create_index(op.f("ix_enquiries_campaign_id"), "enquiries", ["campaign_id"], unique=False)
    op.create_index(op.f("ix_enquiries_store_id"), "enquiries", ["store_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_enquiries_store_id"), table_name="enquiries")
    op.drop_index(op.f("ix_enquiries_campaign_id"), table_name="enquiries")
    op.drop_table("enquiries")

    op.drop_index(op.f("ix_campaigns_store_id"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_start_at"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_is_active"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_end_at"), table_name="campaigns")
    op.drop_table("campaigns")

    op.drop_index(op.f("ix_stores_minor"), table_name="stores")
    op.drop_index(op.f("ix_stores_major"), table_name="stores")
    op.drop_index(op.f("ix_stores_beacon_uuid"), table_name="stores")
    op.drop_table("stores")
