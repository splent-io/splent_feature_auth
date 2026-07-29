"""Add role to user (shared authorization vocabulary for role_required).

New rows default to "user" (least privilege). Pre-existing rows are
backfilled to AUTH_MIGRATION_LEGACY_ROLE, default "admin", because until
this column existed every authenticated user could reach every admin
screen and the backfill preserves exactly that. Products that let
strangers self-register (the signup feature) should run this with
AUTH_MIGRATION_LEGACY_ROLE=user and then promote their real staff with
"splent feature:auth set-role", otherwise every registered visitor keeps
the privileges the missing column used to grant them. The row count is
printed so the promotion is never silent.

Revision ID: auth0002_role
Revises: 990210b54b52
"""

import os

import sqlalchemy as sa
from alembic import op

revision = "auth0002_role"
down_revision = "990210b54b52"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("role", sa.String(length=32), nullable=False, server_default="user"),
    )
    legacy_role = os.getenv("AUTH_MIGRATION_LEGACY_ROLE", "admin").strip() or "admin"
    connection = op.get_bind()
    user_table = sa.table("user", sa.column("role", sa.String(length=32)))
    result = connection.execute(user_table.update().values(role=legacy_role))
    print(
        f"auth0002_role: {result.rowcount} existing user(s) backfilled to "
        f"role '{legacy_role}'. Review them with 'splent feature:auth "
        f"list-users'."
    )


def downgrade():
    op.drop_column("user", "role")
