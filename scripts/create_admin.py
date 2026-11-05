"""Create an admin account, or reset its password if it already exists.

Public registration is disabled, so this is how to get an account to log in
with. The password is prompted for (never passed on the command line) and only
its hash is stored.

Usage, from the project root:

    .venv/bin/python scripts/create_admin.py --email you@example.com --name Paul
    .venv/bin/python scripts/create_admin.py --email you@example.com --db path/to/other.sqlite
"""
import argparse
import asyncio
import getpass
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data import db_session  # noqa: E402
from services import user_service  # noqa: E402

DEFAULT_DB = PROJECT_ROOT / "db" / "saucerdb.sqlite"


def prompt_password() -> str:
    while True:
        password = getpass.getpass("New password: ")
        if len(password) < 5:
            print("Password must be at least 5 characters.")
            continue
        if password != getpass.getpass("Repeat password: "):
            print("Passwords did not match, try again.")
            continue
        return password


async def run(email: str, name: str, password: str) -> None:
    user = await user_service.get_user_by_email(email)
    if user:
        await user_service.set_password(email, password)
        print(f"Password reset for {user.email} (id {user.id}).")
    else:
        user = await user_service.create_account(name, email, password)
        print(f"Created account {user.email} (id {user.id}).")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", default="Admin", help="only used for new accounts")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite file to update")
    args = parser.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        sys.exit(f"Database not found: {db_path}")

    db_session.global_init(db_path.as_posix())
    password = prompt_password()
    asyncio.run(run(args.email, args.name, password))


if __name__ == "__main__":
    main()
