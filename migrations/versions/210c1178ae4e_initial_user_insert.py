"""initial user insert

Revision ID: 210c1178ae4e
Revises: a14af6cf667e
Create Date: 2021-09-09 18:27:32.629715

"""
from datetime import datetime, timezone

from alembic import op
from sqlalchemy import TIMESTAMP, Boolean, String
from sqlalchemy.sql import column, table

from app.domains.entities.user import User

# revision identifiers, used by Alembic.
revision = "210c1178ae4e"
down_revision = "a14af6cf667e"
branch_labels = None
depends_on = None


user_table = table(
    "users",
    column("username", String),
    column("email", String),
    column("account_name", String),
    column("hashed_password", String),
    column("is_active", Boolean),
    column("created_at", TIMESTAMP),
    column("created_by", String),
    column("updated_at", TIMESTAMP),
    column("updated_by", String),
)


def upgrade():
    now = datetime.now(timezone.utc)
    hashed = User.get_hashed_password("plain")
    op.bulk_insert(
        user_table,
        [
            {
                "username": "john",
                "email": "john@example.com",
                "account_name": "ジョン",
                "hashed_password": hashed,
                "is_active": True,
                "created_at": now,
                "created_by": "john",
                "updated_at": now,
                "updated_by": "john",
            },
        ],
    )


def downgrade():
    op.execute("DELETE FROM users WHERE username='john';")
