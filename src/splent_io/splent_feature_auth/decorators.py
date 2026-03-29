from functools import wraps

from flask import abort
from flask_login import current_user, login_required  # noqa: F401
from splent_framework.decorators.decorators import pass_or_abort


def guest_required(f):
    """Require that the user is NOT authenticated (e.g., login/signup pages)."""

    def condition(**kwargs):
        return not current_user.is_authenticated

    return pass_or_abort(condition)(f)


def active_required(f):
    """Require that the user is authenticated AND active (user.active == True)."""

    @login_required
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.active:
            abort(403)
        return f(*args, **kwargs)

    return wrapper


def owner_required(model, url_param="id", owner_field="user_id"):
    """Require that the current user owns the resource.

    Args:
        model: SQLAlchemy model class (e.g., Note).
        url_param: Name of the URL parameter with the resource ID (e.g., "note_id").
        owner_field: Name of the model field that stores the owner's user ID.

    Usage::

        @notes_bp.route("/notes/<int:note_id>/edit")
        @owner_required(Note, "note_id")
        def edit(note_id):
            ...
    """

    def decorator(f):
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            resource_id = kwargs.get(url_param)
            if resource_id is None:
                abort(400)
            resource = model.query.get_or_404(resource_id)
            if getattr(resource, owner_field) != current_user.id:
                abort(403)
            return f(*args, **kwargs)

        return wrapper

    return decorator
