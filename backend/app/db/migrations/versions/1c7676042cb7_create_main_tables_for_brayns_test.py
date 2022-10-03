"""create_main_tables for brayns test

Revision ID: 1c7676042cb7
Revises: 26a079520274
Create Date: 2022-10-03 00:50:14.459526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '1c7676042cb7'
down_revision = '26a079520274'
branch_labels = None
depends_on = None


def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False, server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("bryan_column_test", sa.Numeric(10, 2), nullable=False),
    )

def upgrade() -> None:
    create_cleanings_table()


def downgrade() -> None:
    op.drop_table("cleanings")

