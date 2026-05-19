"""create products table

Revision ID: 72b4ed3cba09
Revises: 0f96014a1d62
Create Date: 2026-05-18 12:38:43.873985

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72b4ed3cba09'
down_revision: Union[str, Sequence[str], None] = '0f96014a1d62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'products',

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
            'category_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'unit_id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'sku',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'barcode',
            sa.String(),
            nullable=True
        ),

        sa.Column(
            'purchase_price',
            sa.Numeric(10, 2),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'selling_price',
            sa.Numeric(10, 2),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'gst_percent',
            sa.Numeric(5, 2),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'opening_stock',
            sa.Numeric(10, 2),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'current_stock',
            sa.Numeric(10, 2),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'minimum_stock',
            sa.Numeric(10, 2),
            nullable=False,
            server_default='0'
        ),

        sa.Column(
            'description',
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

        sa.ForeignKeyConstraint(
            ['category_id'],
            ['categories.id']
        ),

        sa.ForeignKeyConstraint(
            ['unit_id'],
            ['units.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_products_id'),
        'products',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_products_id'),
        table_name='products'
    )

    op.drop_table('products')