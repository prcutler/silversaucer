"""Find mb_id values that aren't MusicBrainz *releases* and fix them.

mb_id should hold a release ID. Hand-entered values sometimes hold a release
group, recording (track), artist or other ID instead, which makes release
lookups fail with 404. For each such record this script:

- clears mb_id, so the next database sync looks the release up again via
  its Discogs link;
- if it was a release group for the same album and the record has no date,
  fills in the release group's original release date;
- keeps any date the record already has.

By default it only checks records that have an mb_id but no date (the ones
that produce 404s). --all checks every stored mb_id (about 1 second each).

Dry run by default. Back up the DB, then run with --apply to write changes.

    .venv/bin/python scripts/fix_mb_kinds.py
    .venv/bin/python scripts/fix_mb_kinds.py --apply
    .venv/bin/python scripts/fix_mb_kinds.py --all
"""
import argparse
import difflib
import re
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.admin_service import identify_mb_entity  # noqa: E402

DEFAULT_DB = PROJECT_ROOT / "db" / "saucerdb.sqlite"


def _normalize(title: str) -> str:
    title = title.lower().replace("&", " and ")
    title = re.sub(r"\([^)]*\)", " ", title)  # "(live)", "(Remastered)"
    title = re.sub(r"\s+-\s+(ep|single)$", " ", title.strip())
    title = re.sub(r"[^\w\s]", " ", title)  # punctuation, curly quotes
    return " ".join(title.split())


def same_album(album_title: str, group_title: str) -> bool:
    """True if a release group's title plausibly names this album.

    Also matches one side of a single, e.g. "For The Animals / Lucifer"
    with the release group "Lucifer".
    """
    group = _normalize(group_title)
    candidates = [_normalize(album_title)]
    candidates += [_normalize(part) for part in album_title.split("/")]
    return any(
        group == c or difflib.SequenceMatcher(None, group, c).ratio() >= 0.85
        for c in candidates
        if c
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--all", action="store_true", help="check every mb_id")
    parser.add_argument("--apply", action="store_true", help="write the changes")
    args = parser.parse_args()

    con = sqlite3.connect(args.db)
    where = "mb_id is not null and trim(mb_id) <> ''"
    if not args.all:
        where += " and (mb_release_date is null or trim(mb_release_date) = '')"
    rows = con.execute(
        "select id, release_id, artist_name, release_title, mb_id, mb_release_date "
        f"from albums where {where} order by artist_name"
    ).fetchall()
    print(f"Checking {len(rows)} MusicBrainz IDs...")

    updates, errors, ok = [], 0, 0
    for n, (row_id, release_id, artist, title, mb_id, date) in enumerate(rows, 1):
        label = f"{artist} - {title} ({release_id})"
        try:
            kind, name, mb_date = identify_mb_entity(mb_id)
        except Exception as e:  # network trouble: skip, don't guess
            errors += 1
            print(f"Skipped, lookup failed: {label}: {e}")
            continue

        if kind == "release":
            ok += 1
            if n % 50 == 0:
                print(f"  ...{n}/{len(rows)} checked")
            continue

        new_date = date
        if kind is None:
            note = "not found on MusicBrainz"
        elif kind == "release-group" and same_album(title, name):
            note = f'release group "{name}", same album'
            if not (date or "").strip() and mb_date:
                new_date = mb_date
                note += f", date {mb_date}"
        else:
            note = f'{kind} "{name}"'
            if kind == "release-group":
                note += ", DIFFERENT album"

        if (date or "").strip() and kind == "release-group" and not same_album(title, name or ""):
            note += f" (kept existing date {date.strip()}; check it)"
        print(f"Clear ID: {label}: {note}")
        updates.append((new_date, row_id))

    print()
    print(f"OK (releases): {ok}  To fix: {len(updates)}  Lookup errors: {errors}")

    if args.apply:
        with con:
            con.executemany(
                "update albums set mb_id = null, mb_release_date = ? where id = ?",
                updates,
            )
        print("Changes written.")
    else:
        print("Dry run, nothing written. Re-run with --apply to save.")


if __name__ == "__main__":
    main()
