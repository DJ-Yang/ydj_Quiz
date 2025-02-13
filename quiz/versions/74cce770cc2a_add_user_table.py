"""add user table


Revision ID: 74cce770cc2a
Revises: 
Create Date: 2025-02-13 14:46:22.320791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74cce770cc2a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("nickname", sa.String(length=20), nullable=False, comment="별명"),
        sa.Column("password", sa.String(length=64), nullable=False, comment="비밀번호"),
        sa.Column("created_dt", sa.DateTime(), nullable=False),
        sa.Column("updated_dt", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("nickname"),
    )


def downgrade() -> None:
    op.drop_table("user")
