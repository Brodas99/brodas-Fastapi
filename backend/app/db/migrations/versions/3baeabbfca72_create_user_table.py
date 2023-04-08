"""create_user_table

Revision ID: 3baeabbfca72
Revises: 55e9205dffdf
Create Date: 2023-04-07 20:15:04.293251

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3baeabbfca72'
down_revision = '55e9205dffdf'
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )
def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )

def create_users_table() -> None:
    op.create_table(
        "users_v1",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("firstname", sa.Text, unique=True, nullable=False, index=True), 
        sa.Column("lastname", sa.Text, unique=True, nullable=False, index=True), 
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),        
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="True"),    
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users_v1
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )
def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
def downgrade() -> None: 
    op.drop_table("users_v1")
    op.execute("DROP FUNCTION update_updated_at_column")
