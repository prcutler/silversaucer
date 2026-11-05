"""Signed login cookie.

The cookie value is "<user_id>:<expires>:<signature>", where the signature is an
HMAC-SHA256 of "<user_id>:<expires>" using a secret key that only the server
knows. Without the key, nobody can produce a valid cookie for a user id.

Configuration (environment variables take priority over data/config.py):

- SILVERSAUCER_SECRET_KEY / config.secret_key: required in production. Generate
  one with:  python -c "import secrets; print(secrets.token_hex(32))"
- SILVERSAUCER_SECURE_COOKIES=1 / config.secure_cookies = True: only send the
  cookie over HTTPS. Turn on in production; leave off for http://127.0.0.1.
"""
import hashlib
import hmac
import os
import secrets
import time
from typing import Optional

from fastapi import Request, Response

from infrastructure.num_convert import try_int

auth_cookie_name = "silver_saucer"
COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 days


def _config_value(name: str, default=None):
    try:
        from data import config
    except ImportError:
        return default
    return getattr(config, name, default)


def _load_secret_key() -> bytes:
    key = os.environ.get("SILVERSAUCER_SECRET_KEY") or _config_value("secret_key")
    if not key:
        print(
            "WARNING: SILVERSAUCER_SECRET_KEY is not set. Using a random key, so "
            "logins reset on every restart and don't work across multiple "
            "workers. Set it in production."
        )
        key = secrets.token_hex(32)
    return key.encode("utf-8")


def _load_secure_flag() -> bool:
    env = os.environ.get("SILVERSAUCER_SECURE_COOKIES")
    if env is not None:
        return env.strip().lower() in ("1", "true", "yes", "on")
    return bool(_config_value("secure_cookies", False))


_secret_key = _load_secret_key()
_secure_cookies = _load_secure_flag()


def _sign(payload: str) -> str:
    return hmac.new(_secret_key, payload.encode("utf-8"), hashlib.sha256).hexdigest()


def set_auth(response: Response, user_id: int):
    expires = int(time.time()) + COOKIE_MAX_AGE
    payload = f"{user_id}:{expires}"
    response.set_cookie(
        auth_cookie_name,
        f"{payload}:{_sign(payload)}",
        max_age=COOKIE_MAX_AGE,
        secure=_secure_cookies,
        httponly=True,
        samesite="Lax",
    )


def get_user_id_via_auth_cookie(request: Request) -> Optional[int]:
    val = request.cookies.get(auth_cookie_name)
    if not val:
        return None

    parts = val.split(":")
    if len(parts) != 3:
        # Includes cookies in the old unsigned format; the user logs in again.
        return None

    user_id, expires, signature = parts
    if not hmac.compare_digest(signature, _sign(f"{user_id}:{expires}")):
        print("Warning: invalid auth cookie signature")
        return None

    if try_int(expires) < time.time():
        return None

    return try_int(user_id) or None


def logout(response: Response):
    response.delete_cookie(auth_cookie_name)
