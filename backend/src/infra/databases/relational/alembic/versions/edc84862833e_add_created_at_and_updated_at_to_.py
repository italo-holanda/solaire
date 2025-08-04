"""add created_at and updated_at to CategoryModel

Revision ID: edc84862833e
Revises: 
Create Date: 2025-07-11 06:08:29.521317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edc84862833e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Adds created_at, updated_at and deleted_at columns ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Removes created_at, updated_at and deleted_at columns ###
    pass
    # ### end Alembic commands ###
