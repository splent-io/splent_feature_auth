from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service
from flask_login import LoginManager

from splent_io.splent_feature_auth.services import AuthenticationService

auth_bp = create_blueprint(__name__)


def init_feature(app):
    from .models import User

    register_service(app, "AuthenticationService", AuthenticationService)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        # Login already refuses disabled accounts (UserRepository.get_by_email
        # filters on active). Refusing them here too means deactivating an
        # account ends its live sessions and remember-me cookies instead of
        # letting them run until expiry.
        user = User.query.get(int(user_id))
        return user if user is not None and user.active else None

    app.login_manager = login_manager


def inject_context_vars(app):
    return {}
