from typing import Optional

import data.config as config
from data.user import User


def login_user(username: str, password: str) -> Optional[User]:
    if password == config.password:
        return User(username, password)

    return None
