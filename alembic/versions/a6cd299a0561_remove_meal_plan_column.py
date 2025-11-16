"""remove_meal_plan_column

Revision ID: a6cd299a0561
Revises: 272f9afcdb98
Create Date: 2025-11-15 20:55:37.871005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6cd299a0561'
down_revision = '272f9afcdb98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remove accepts_meal_plan column from vendors table
    op.drop_column('vendors', 'accepts_meal_plan')


def downgrade() -> None:
    # Re-add accepts_meal_plan column if needed to rollback
    op.add_column('vendors', sa.Column('accepts_meal_plan', sa.Boolean(), nullable=False, server_default=sa.text('true')))

