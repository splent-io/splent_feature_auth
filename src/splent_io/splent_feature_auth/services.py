import os

from blinker import Namespace
from flask_login import login_user, current_user

from splent_io.splent_feature_auth.models import User
from splent_io.splent_feature_auth.repositories import UserRepository
from splent_framework.configuration.configuration import uploads_folder_name
from splent_framework.services.BaseService import BaseService


# Signals — features that depend on auth can connect to these
auth_signals = Namespace()
user_registered = auth_signals.signal("user-registered")


class AuthenticationService(BaseService):

    def __init__(self, user_repository=None):
        super().__init__(user_repository or UserRepository())

    def login(self, email, password, remember=True):
        user = self.repository.get_by_email(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            return True
        return False

    def is_email_available(self, email: str) -> bool:
        return self.repository.get_by_email(email) is None

    def create_user(self, **kwargs):
        """Create a User only. Emits user_registered signal for dependent features."""
        try:
            email = kwargs.pop("email", None)
            password = kwargs.pop("password", None)

            if not email:
                raise ValueError("Email is required.")
            if not password:
                raise ValueError("Password is required.")

            user_data = {
                "email": email,
                "password": password,
                "active": False,
            }
            user = self.create(**user_data)

            # Emit signal — profile, confirmemail, etc. can react
            from flask import current_app
            user_registered.send(current_app._get_current_object(), user=user, **kwargs)

            return user
        except Exception as exc:
            self.repository.session.rollback()
            raise exc

    def get_authenticated_user(self) -> User | None:
        if current_user.is_authenticated:
            return current_user
        return None

    def temp_folder_by_user(self, user: User) -> str:
        return os.path.join(uploads_folder_name(), "temp", str(user.id))

    def get_by_email(self, email: str, active: bool = True) -> User:
        return self.repository.get_by_email(email, active)
