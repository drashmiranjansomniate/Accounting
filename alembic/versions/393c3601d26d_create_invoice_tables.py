"""create invoice tables

Revision ID: 393c3601d26d
Revises: 7c99116adb30
Create Date: 2026-05-15 15:29:15.750199
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '393c3601d26d'

down_revision: Union[str, Sequence[str], None] = '7c99116adb30'

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'sales_invoices',

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
            'customer_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'sales_order_id',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'invoice_number',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'status',
            sa.Enum(
                'DRAFT',
                'SENT',
                'PARTIALLY_PAID',
                'PAID',
                'OVERDUE',
                'CANCELLED',
                name='invoicestatus'
            ),
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
            'paid_amount',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'due_amount',
            sa.Float(),
            nullable=True
        ),

        sa.Column(
            'notes',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'due_date',
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            'created_by',
            sa.Integer(),
            nullable=True
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=True
        ),

        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['created_by'],
            ['users.id']
        ),

        sa.ForeignKeyConstraint(
            ['customer_id'],
            ['customers.id']
        ),

        sa.ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id']
        ),

        sa.ForeignKeyConstraint(
            ['sales_order_id'],
            ['sales_orders.id']
        ),

        sa.PrimaryKeyConstraint('id'),

        sa.UniqueConstraint('invoice_number')
    )

    op.create_index(
        op.f('ix_sales_invoices_id'),
        'sales_invoices',
        ['id'],
        unique=False
    )

    op.create_table(
        'sales_invoice_items',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'invoice_id',
            sa.Integer(),
            nullable=True
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
        ),

        sa.ForeignKeyConstraint(
            ['invoice_id'],
            ['sales_invoices.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_sales_invoice_items_id'),
        'sales_invoice_items',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_sales_invoice_items_id'),
        table_name='sales_invoice_items'
    )

    op.drop_table('sales_invoice_items')

    op.drop_index(
        op.f('ix_sales_invoices_id'),
        table_name='sales_invoices'
    )

    op.drop_table('sales_invoices')