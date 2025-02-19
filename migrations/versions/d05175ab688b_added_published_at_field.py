"""Added published at field

Revision ID: d05175ab688b
Revises: 8b5bf2e18310
Create Date: 2025-02-19 17:41:05.829469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd05175ab688b'
down_revision: Union[str, None] = '8b5bf2e18310'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Bind to current DB connection
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Get existing columns in the table
    columns = [col['name'] for col in inspector.get_columns('article_saved')]

    # Only add the column if it doesn't exist
    if 'published_at' not in columns:
        # MySQL-specific syntax to add a column after another column
        op.execute("""
            ALTER TABLE article_saved
            ADD COLUMN published_at VARCHAR(150) DEFAULT NULL
            AFTER sentiment
        """)


def downgrade() -> None:
    # In case you want to remove the column on downgrade
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('article_saved')]

    if 'published_at' in columns:
        op.execute("""
            ALTER TABLE article_saved
            DROP COLUMN published_at
        """)
