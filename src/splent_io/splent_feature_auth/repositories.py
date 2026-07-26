from splent_io.splent_feature_auth.models import User
from splent_framework.repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def create(self, commit: bool = True, **kwargs):
        password = kwargs.pop("password")
        instance = self.model(**kwargs)
        instance.set_password(password)
        self.session.add(instance)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return instance

    def get_by_email(self, email: str, active: bool = True):
        return self.model.query.filter_by(email=email, active=active).first()

    def email_exists(self, email: str) -> bool:
        """Whether the address is taken, in any account state.

        get_by_email filters on active because login must ignore disabled
        accounts. Availability is a different question: sign-up creates users
        inactive, so an active-only check reports a just-registered address as
        free and the insert then dies on the unique index.
        """
        return self.model.query.filter_by(email=email).first() is not None
