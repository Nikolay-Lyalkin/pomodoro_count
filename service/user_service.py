import datetime as dt
import os
from datetime import timedelta

import dotenv
from fastapi import HTTPException, Security, security
from jose import jwt

from exceptions import TokenExpired

dotenv.load_dotenv()


class UserService:

    @staticmethod
    def generate_access_token(user_id):
        expire_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode({"user_id": user_id, "expire": expire_date_unix}, os.getenv("SECRET_ACCESS_TOKEN"),
                           os.getenv("ALGORITHM_ACCESS_TOKEN"))
        return token

    @staticmethod
    def get_user_id_from_access_token(access_token: str) -> int:
        payload = jwt.decode(access_token, os.getenv("SECRET_ACCESS_TOKEN"),
                             algorithms=[os.getenv("ALGORITHM_ACCESS_TOKEN")])
        if payload["expire"] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
        return payload["user_id"]
