"""Merge multiple heads into a single head

Revision ID: merge_heads_20251115
Revises: 1d831e460f9a, update_vendors_hours_20251115
Create Date: 2025-11-15 17:40:00

This migration is a no-op merge to unify two branch heads so `alembic upgrade head` works.
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'merge_heads_20251115'
down_revision: Union[str, Sequence[str], None] = ('1d831e460f9a', 'update_vendors_hours_20251115')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This is a merge commit for Alembic migration history. No schema changes.
    pass


def downgrade() -> None:
    # Nothing to revert; this is only a history merge.
    pass
