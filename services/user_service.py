import asyncio
import datetime
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.future import select

from data import db_session
from data.user import User

# Stored hashes look like "$6$rounds=172434$<salt>$<hash>": the salt and
# settings are part of the string, so verify() re-hashes the typed password
# with them and compares. To move to a stronger scheme later, put it first in
# `schemes` (e.g. ["argon2", "sha512_crypt"]); with deprecated="auto", old
# hashes still verify and are upgraded automatically on the next login.
pwd_context = CryptContext(
    schemes=["sha512_crypt"],
    deprecated="auto",
    sha512_crypt__rounds=172_434,
)


def normalize_email(email: Optional[str]) -> str:
    return (email or "").strip().lower()


async def user_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(User.id))
        result = await session.execute(query)
        return result.scalar()


async def create_account(name: str, email: str, password: str) -> User:
    user = User()
    user.email = normalize_email(email)
    user.name = name
    user.hash_password = pwd_context.hash(password)

    async with db_session.create_async_session() as session:
        session.add(user)
        await session.commit()

    return user


async def set_password(email: str, password: str) -> Optional[User]:
    """Replace a user's password hash. Returns None if the email is unknown."""
    async with db_session.create_async_session() as session:
        user = await _find_by_email(session, email)
        if not user:
            return None

        user.hash_password = pwd_context.hash(password)
        await session.commit()
        return user


async def login_user(email: str, password: str) -> Optional[User]:
    """Return the user if the email and password match, otherwise None.

    The reason for a failure is logged on the server only; callers should show
    the same generic message either way.
    """
    async with db_session.create_async_session() as session:
        user = await _find_by_email(session, email)
        if not user:
            print(f"Login failed: no account for {normalize_email(email)!r}")
            return None

        try:
            # ~0.05s of CPU per check; keep it off the event loop.
            valid, new_hash = await asyncio.to_thread(
                pwd_context.verify_and_update, password, user.hash_password
            )
        except (ValueError, TypeError):
            print(
                f"Login failed: stored password for user {user.id} is not a "
                "recognised hash format; reset it with scripts/create_admin.py"
            )
            return None

        if not valid:
            print(f"Login failed: wrong password for user {user.id}")
            return None

        if new_hash:
            # The stored hash used old settings or a deprecated scheme.
            user.hash_password = new_hash
        user.last_login = datetime.datetime.now()
        await session.commit()

        return user


async def _find_by_email(session, email: str) -> Optional[User]:
    query = select(User).filter(func.lower(User.email) == normalize_email(email))
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()


async def get_user_by_email(email: str) -> Optional[User]:
    async with db_session.create_async_session() as session:
        return await _find_by_email(session, email)
