"""add quiz table

Revision ID: 4298d554273a
Revises: 74cce770cc2a
Create Date: 2025-02-13 21:38:45.895192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4298d554273a'
down_revision: Union[str, None] = '74cce770cc2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'problem',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(256), nullable=False, comment='문제 제목'),
        sa.Column('created_dt', sa.DateTime(), nullable=False),
        sa.Column('updated_dt', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('id'),
    )
    
    op.create_table(
        'selection',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('problem_id', sa.Integer(), sa.ForeignKey('problem.id', ondelete='CASCADE'), nullable=False, comment='문제 ID'),
        sa.Column('content', sa.String(256), nullable=False, comment='문제 보기'),
        sa.Column('is_correct', sa.Boolean(), nullable=False, server_default=sa.false(), comment='정답 여부'),
        sa.Column('created_dt', sa.DateTime(), nullable=False),
        sa.Column('updated_dt', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('id'),
    )
    
    op.create_table(
        'user_problem_form',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, comment='작성자 ID'),
        sa.Column('problem_id', sa.Integer(), sa.ForeignKey('problem.id', ondelete='CASCADE'), nullable=False, comment='문제 ID'),
        sa.Column('choices', sa.Text(), nullable=False, comment='제출지'),
        sa.Column('score', sa.String(8), nullable=True, comment='점수'),
        sa.Column('created_dt', sa.DateTime(), nullable=False),
        sa.Column('updated_dt', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('id'),
    )

def downgrade() -> None:
    op.drop_table('user_problem_form')
    op.drop_table('selection')
    op.drop_table('problem')