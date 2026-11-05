"""One-time cleanup of MusicBrainz IDs and dates in the albums table.

- Trims spaces/tabs from mb_id and mb_release_date; blank values become NULL
  so the import treats them as missing and looks them up.
- Reduces pasted web addresses (".../cover-art", "/<id>") to the bare ID.
- Release-group IDs are cleared from mb_id (it holds release IDs). If the
  album has no date, the release group's original release date is filled in.
- Fills in the original release date for any ID it fixed that has no date.

Dry run by default: it prints what would change. Back up the DB, then run
with --apply to write the changes.

    .venv/bin/python scripts/clean_mb_data.py
    .venv/bin/python scripts/clean_mb_data.py --apply
"""
import argparse
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import musicbrainzngs  # noqa: E402

from infrastructure.mb_ids import RELEASE_GROUP, clean_date, parse_mb_id  # noqa: E402
from services.admin_service import _original_release_date  # noqa: E402

DEFAULT_DB = PROJECT_ROOT / "db" / "saucerdb.sqlite"


def group_first_release_date(group_id: str):
    try:
        group = musicbrainzngs.get_release_group_by_id(group_id)["release-group"]
    except musicbrainzngs.WebServiceError as e:
        print("  MusicBrainz release group lookup failed for", group_id, e)
        return None
    return group.get("first-release-date") or None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args()

    con = sqlite3.connect(args.db)
    rows = con.execute(
        "select id, release_id, artist_name, release_title, mb_id, mb_release_date "
        "from albums order by artist_name"
    ).fetchall()

    counts = {"blank id": 0, "trimmed id": 0, "url fixed": 0, "release group": 0,
              "date trimmed": 0, "date fetched": 0, "unparseable": 0}
    updates = []

    for row_id, release_id, artist, title, mb_id, date in rows:
        label = f"{artist} - {title} ({release_id})"
        new_date = clean_date(date)
        if date is not None and new_date != date:
            counts["date trimmed"] += 1

        try:
            kind, new_id = parse_mb_id(mb_id)
        except ValueError:
            counts["unparseable"] += 1
            print(f"Left alone, no ID found: {label}: {mb_id!r}")
            new_id, kind = mb_id, None

        needs_date = False
        if mb_id is not None and kind is None and new_id is None:
            counts["blank id"] += 1
        elif kind == RELEASE_GROUP:
            counts["release group"] += 1
            print(f"Release group cleared: {label}: {mb_id!r}")
            if not new_date:
                needs_date = ("group", new_id)
            new_id = None
        elif new_id and new_id != mb_id:
            if new_id == mb_id.strip():
                counts["trimmed id"] += 1
            else:
                counts["url fixed"] += 1
                print(f"Address reduced to ID: {label}: {mb_id!r} -> {new_id}")
            if not new_date:
                needs_date = ("release", new_id)

        if needs_date:
            if args.apply:
                kind_, the_id = needs_date
                new_date = (group_first_release_date(the_id) if kind_ == "group"
                            else _original_release_date(the_id))
                print(f"  date fetched: {new_date}")
            else:
                print("  (would fetch the original release date)")
            counts["date fetched"] += 1

        if (new_id, new_date) != (mb_id, date):
            updates.append((new_id, new_date, row_id))

    print()
    for name, n in counts.items():
        print(f"{name:>14}: {n}")
    print(f"{'rows changed':>14}: {len(updates)}")

    if args.apply:
        with con:
            con.executemany(
                "update albums set mb_id = ?, mb_release_date = ? where id = ?", updates
            )
        print("Changes written.")
    else:
        print("Dry run, nothing written. Re-run with --apply to save.")


if __name__ == "__main__":
    main()
