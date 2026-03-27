"""Alembic migration environment for splent_feature_auth."""

from splent_io.splent_feature_auth import models  # noqa: F401
from splent_framework.migrations.feature_env import run_feature_migrations

FEATURE_NAME = "splent_feature_auth"
FEATURE_TABLES = {"user"}

run_feature_migrations(FEATURE_NAME, FEATURE_TABLES)
