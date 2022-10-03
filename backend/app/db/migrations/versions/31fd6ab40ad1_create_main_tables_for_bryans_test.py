"""create_main_tables for bryans test

Revision ID: 31fd6ab40ad1
Revises: 1c7676042cb7
Create Date: 2022-10-03 00:52:24.063678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '31fd6ab40ad1'
down_revision = '1c7676042cb7'
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.add_column('cleanings', sa.Column('last_transaction_date', sa.DateTime))


def downgrade() -> None:
    op.drop_table("cleanings", 'last_transaction_date')
