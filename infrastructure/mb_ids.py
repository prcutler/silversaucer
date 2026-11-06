"""Clean up MusicBrainz IDs and dates entered by hand or stored in the DB.

People paste all sorts of things into the MusicBrainz ID field: the bare ID,
a full web address, the ID with spaces around it, or an address with extra
path on the end ("/cover-art"). These helpers reduce that to a bare ID and say
whether it is a release or a release group.
"""
import re
from typing import Optional, Tuple

_MB_UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
_MB_REF = re.compile(rf"(?:(release-group|release)/)?({_MB_UUID})")

RELEASE = "release"
RELEASE_GROUP = "release-group"


def parse_mb_id(text: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Return (kind, bare_id) for whatever was entered.

    - blank or None              -> (None, None)
    - bare ID or .../release/ID  -> ("release", id)
    - .../release-group/ID       -> ("release-group", id)
    - anything else              -> raises ValueError

    A bare ID with no "release-group/" in front is assumed to be a release,
    since that is what the mb_id column holds.
    """
    text = (text or "").strip()
    if not text:
        return None, None

    match = _MB_REF.search(text)
    if not match:
        raise ValueError(f"No MusicBrainz ID found in {text!r}")

    kind = match.group(1) or RELEASE
    return kind, match.group(2).lower()


def clean_date(text: Optional[str]) -> Optional[str]:
    """Strip spaces and tabs from a date; blank becomes None."""
    text = (text or "").strip()
    return text or None


def normalize_title(title: Optional[str]) -> str:
    """Lower-case a title and drop punctuation, "(...)" parts and a trailing
    " - EP", so Discogs and MusicBrainz spellings of one title compare equal.
    "Live From The Ryman Vol. 2 " and "Live from the Ryman, Vol. 2" -> same."""
    title = (title or "").lower().replace("&", " and ")
    title = re.sub(r"\([^)]*\)", " ", title)
    title = re.sub(r"\s+-\s+(ep|single)$", " ", title.strip())
    title = re.sub(r"[^\w\s]", " ", title)
    return " ".join(title.split())


def normalize_artist(name: Optional[str]) -> str:
    """Like normalize_title, plus Discogs quirks: "Momma (6)" -> "momma",
    "Various" -> "various artists"."""
    name = re.sub(r"\s*\(\d+\)$", "", (name or "").strip())
    name = normalize_title(name)
    return "various artists" if name == "various" else name
