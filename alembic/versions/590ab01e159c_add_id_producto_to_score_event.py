"""add id_producto to score_event

Revision ID: 590ab01e159c
Revises: e0e54e13184d
Create Date: 2025-11-06 19:28:49.968101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '590ab01e159c'
down_revision: Union[str, Sequence[str], None] = 'e0e54e13184d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
