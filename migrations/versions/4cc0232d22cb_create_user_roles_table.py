"""create user_roles table

Revision ID: 4cc0232d22cb
Revises: beaa9ca1dde7
Create Date: 2021-09-14 18:48:58.266107

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4cc0232d22cb"
down_revision = "beaa9ca1dde7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_roles",
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["username"],
            ["users.username"],
        ),
        sa.PrimaryKeyConstraint("username", "role_id"),
        sa.UniqueConstraint("username", "role_id", name="unique_user_role"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_roles")
    # ### end Alembic commands ###
