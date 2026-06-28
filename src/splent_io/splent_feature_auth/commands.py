"""CLI commands contributed by the auth feature.

Exposed under the ``feature:auth`` group, e.g.::

    splent feature:auth set-password user@example.com
    splent feature:auth list-users
    splent feature:auth create-user new@example.com

They run inside the active product's Flask app context, so they reach the
product database directly through SQLAlchemy.
"""

import click

from splent_framework.db import db
from splent_io.splent_feature_auth.models import User


@click.command("set-password")
@click.argument("email")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="New password (prompted securely if omitted).",
)
def set_password(email, password):
    """Change ANY user's password, by email."""
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise click.ClickException(f"No user with email '{email}'.")
    user.set_password(password)
    db.session.commit()
    click.secho(f"  Password updated for {email}.", fg="green")


@click.command("list-users")
def list_users():
    """List all users in the active product."""
    users = User.query.order_by(User.id).all()
    if not users:
        click.secho("  No users.", fg="yellow")
        return
    click.echo()
    for u in users:
        state = (
            click.style("active", fg="green")
            if u.active
            else click.style("inactive", fg="red")
        )
        click.echo(f"  #{u.id:<4} {u.email or '(no email)':<32} [{state}]")
    click.echo()


@click.command("create-user")
@click.argument("email")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password for the new user.",
)
def create_user(email, password):
    """Create a new user."""
    if User.query.filter_by(email=email).first():
        raise click.ClickException(f"A user with email '{email}' already exists.")
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    click.secho(f"  Created user {email}.", fg="green")


cli_commands = [set_password, list_users, create_user]
