"""articles table modified

Revision ID: 3c9d7cfd695b
Revises: c7d3b4cedb0d
Create Date: 2025-03-17 00:03:02.363102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c9d7cfd695b'
down_revision: Union[str, None] = 'c7d3b4cedb0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Create a new migration with: alembic revision --autogenerate -m "create articles table"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('abstract', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['content.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('articles')

