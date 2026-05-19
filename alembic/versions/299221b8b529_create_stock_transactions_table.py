"""create stock transactions table

Revision ID: STOCK_TXN_001
Revises: 72b4ed3cba09
Create Date: 2026-05-18

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'STOCK_TXN_001'
down_revision: Union[str, Sequence[str], None] = '72b4ed3cba09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'stock_transactions',

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
            'product_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'transaction_type',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'quantity',
            sa.Numeric(10, 2),
            nullable=False
        ),

        sa.Column(
            'before_stock',
            sa.Numeric(10, 2),
            nullable=False
        ),

        sa.Column(
            'after_stock',
            sa.Numeric(10, 2),
            nullable=False
        ),

        sa.Column(
            'reference_type',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'reference_id',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'remarks',
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id']
        ),

        sa.ForeignKeyConstraint(
            ['product_id'],
            ['products.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_stock_transactions_id'),
        'stock_transactions',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_stock_transactions_id'),
        table_name='stock_transactions'
    )

    op.drop_table('stock_transactions')
