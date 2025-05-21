import random
import string


class UserService:

    @staticmethod
    def generate_access_token():
        token = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return token
