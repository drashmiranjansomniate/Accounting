"""create categories table

Revision ID: c2e7778eb5bf
Revises: 393c3601d26d
Create Date: 2026-05-18 11:36:17.611252

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2e7778eb5bf'
down_revision: Union[str, Sequence[str], None] = '393c3601d26d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'categories',

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
            'description',
            sa.Text(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id']
        ),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_categories_id'),
        'categories',
        ['id'],
        unique=False
    )


def downgrade() -> None:

    op.drop_index(
        op.f('ix_categories_id'),
        table_name='categories'
    )

    op.drop_table('categories')