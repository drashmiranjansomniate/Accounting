"""create units table

Revision ID: 0f96014a1d62
Revises: c2e7778eb5bf
Create Date: 2026-05-18 12:21:49.850251

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f96014a1d62'
down_revision: Union[str, Sequence[str], None] = 'c2e7778eb5bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'units',

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
            'short_name',
            sa.String(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_units_id'),
        'units',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_units_id'),
        table_name='units'
    )

    op.drop_table('units')