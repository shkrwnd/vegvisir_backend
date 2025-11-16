"""add_latitude_longitude_to_vendors

Revision ID: 59a998326b34
Revises: a6cd299a0561
Create Date: 2025-11-15 21:39:15.628133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59a998326b34'
down_revision = 'a6cd299a0561'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add latitude and longitude columns to vendors table
    op.add_column('vendors', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('vendors', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    # Remove latitude and longitude columns
    op.drop_column('vendors', 'longitude')
    op.drop_column('vendors', 'latitude')

