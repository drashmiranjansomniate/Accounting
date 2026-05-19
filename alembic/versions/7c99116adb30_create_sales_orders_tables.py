"""create sales orders tables

Revision ID: 7c99116adb30
Revises: 499f5c3f73ad
Create Date: 2026-05-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7c99116adb30'
down_revision: Union[str, Sequence[str], None] = '499f5c3f73ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'sales_orders',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            'organization_id',
            sa.Integer(),
            sa.ForeignKey('organizations.id'),
            nullable=False
        ),

        sa.Column(
            'customer_id',
            sa.Integer(),
            sa.ForeignKey('customers.id'),
            nullable=False
        ),

        sa.Column(
            'quotation_id',
            sa.Integer(),
            sa.ForeignKey('quotations.id'),
            nullable=True
        ),

        sa.Column(
            'sales_order_number',
            sa.String(),
            nullable=False,
            unique=True
        ),

        sa.Column(
            'status',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'priority',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'subtotal',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'tax_amount',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'total_amount',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'notes',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'expected_delivery_date',
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            'created_by',
            sa.Integer(),
            sa.ForeignKey('users.id'),
            nullable=True
        ),

        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()')
        ),

        sa.Column(
            'updated_at',
            sa.DateTime(),
            nullable=True
        )
    )

    op.create_table(
        'sales_order_items',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            'sales_order_id',
            sa.Integer(),
            sa.ForeignKey('sales_orders.id')
        ),

        sa.Column(
            'item_name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'quantity',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'price',
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            'tax_percent',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'total',
            sa.Float(),
            nullable=False
        )
    )


def downgrade() -> None:

    op.drop_table('sales_order_items')

    op.drop_table('sales_orders')