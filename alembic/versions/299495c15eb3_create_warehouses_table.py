"""create warehouses table

Revision ID: 299495c15eb3
Revises: STOCK_TXN_001
Create Date: 2026-05-18

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '299495c15eb3'
down_revision: Union[str, Sequence[str], None] = 'STOCK_TXN_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'warehouses',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'organization_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'code',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'address',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=True,
            server_default=sa.text('true')
        ),

        sa.ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_warehouses_id'),
        'warehouses',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_warehouses_id'),
        table_name='warehouses'
    )

    op.drop_table('warehouses')