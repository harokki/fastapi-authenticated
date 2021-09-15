"""create initial role and user_role

Revision ID: 490ab0ac3067
Revises: 4cc0232d22cb
Create Date: 2021-09-15 12:20:28.001869

"""
from alembic import op
from sqlalchemy import String
from sqlalchemy.sql import column, table

from app.domains.entities.role import Role

# revision identifiers, used by Alembic.
revision = "490ab0ac3067"
down_revision = "4cc0232d22cb"
branch_labels = None
depends_on = None

role_table = table(
    "roles", column("id", String), column("name", String), column("description", String)
)

user_role_table = table(
    "user_roles", column("username", String), column("role_id", String)
)

admin_role = Role("Admin", "Admin of Application Ecosystem")
guest_role = Role("Guest", "Guest User")


def upgrade():

    op.bulk_insert(
        role_table,
        [
            {
                "id": admin_role.id,
                "name": admin_role.name,
                "description": admin_role.description,
            },
            {
                "id": guest_role.id,
                "name": guest_role.name,
                "description": guest_role.description,
            },
        ],
    )
    op.bulk_insert(user_role_table, [{"username": "john", "role_id": admin_role.id}])


def downgrade():
    op.execute(f"DELETE FROM roles WHERE id = '{admin_role.id}'")
    op.execute(f"DELETE FROM roles WHERE id = '{guest_role.id}'")
    op.execute("DELETE FROM user_roles WHERE username = 'john'")
