from flask_login import UserMixin

user_database = {}

class User(UserMixin):
    """
    Simple User model backed by dict in memory.
    """

    def __init__(self, username):
        self.id = username
        self.username = username

    @staticmethod
    def get(user_id):
        return user_database.get(user_id)

    @classmethod
    def create(class_, username):
        user = class_(username)
        user_database[username] = user
        return user

    @classmethod
    def get_or_create(class_, username):
        user = User.get(username)
        if user is None:
            user = class_.create(username)
        return user
