import hashlib
from typing import Optional

from fastapi import Request, Response

from infrastructure.num_convert import try_int

auth_cookie_name = "pypi_account"


def set_auth(response: Response, user_id: int):
    hash_val = __hash_text(str(user_id))
    val = "{}:{}".format(user_id, hash_val)
    response.set_cookie(
        auth_cookie_name, val, secure=False, httponly=True, samesite="Lax"
    )


def __hash_text(text: str) -> str:
    text = "salty__" + text + "__text"
    return hashlib.sha512(text.encode("utf-8")).hexdigest()


def get_user_id_via_auth_cookie(request: Request) -> Optional[int]:
    if auth_cookie_name not in request.cookies:
        return None

    val = request.cookies[auth_cookie_name]
    parts = val.split(":")
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]
    hash_val_check = __hash_text(user_id)
    if hash_val != hash_val_check:
        print("Warning: Hash mismatch, invalid cookie value")
        return None

    return try_int(user_id)


def logout(response: Response):
    response.delete_cookie(auth_cookie_name)
