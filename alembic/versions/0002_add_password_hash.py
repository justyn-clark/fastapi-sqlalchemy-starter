import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_add_password_hash"
down_revision = "0001_create_users"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "password_hash", sa.String(length=255), nullable=False, server_default=""
        ),
    )
    op.alter_column("users", "password_hash", server_default=None)

def downgrade() -> None:
    op.drop_column("users", "password_hash")
