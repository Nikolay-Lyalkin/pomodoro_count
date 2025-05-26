class UserNotFound(Exception):
    detail = "username or password don't match"


class TokenExpired(Exception):
    detail = "token has expired"


class TaskNotFound(Exception):
    detail = "task not found"
