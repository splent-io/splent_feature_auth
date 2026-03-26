from splent_io.splent_feature_auth.models import User
from splent_framework.seeders.BaseSeeder import BaseSeeder


class AuthSeeder(BaseSeeder):

    priority = 1

    def run(self):
        users = [
            User(email="user1@example.com", password="1234"),
            User(email="user2@example.com", password="1234"),
        ]
        self.seed(users)
