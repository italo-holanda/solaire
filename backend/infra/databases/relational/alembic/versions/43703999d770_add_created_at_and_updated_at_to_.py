"""add created_at and updated_at to CategoryModel

Revision ID: 43703999d770
Revises: edc84862833e
Create Date: 2025-07-11 06:13:54.684081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43703999d770'
down_revision: Union[str, Sequence[str], None] = 'edc84862833e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Add columns as nullable, no default
    op.add_column('categories', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('categories', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('categories', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))

    # 2. Set current timestamp for existing rows
    from sqlalchemy.sql import table, column
    from sqlalchemy import DateTime, func
    categories = table('categories',
        column('created_at', DateTime(timezone=True)),
        column('updated_at', DateTime(timezone=True)),
    )
    op.execute(
        categories.update().values(
            created_at=func.now(),
            updated_at=func.now()
        )
    )

    # 3. (Optional) If you want to enforce NOT NULL, you must recreate the table in SQLite.
    # Otherwise, handle NOT NULL/default at the application/model level.


def downgrade() -> None:
    """Downgrade schema."""
    # Removes created_at, updated_at and deleted_at columns ###
    op.drop_column('categories', 'deleted_at')
    op.drop_column('categories', 'updated_at')
    op.drop_column('categories', 'created_at')
    # ### end Alembic commands ###

