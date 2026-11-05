"""Discogs collection folder id -> format name shown on the site.

The sync stores each album's Discogs folder id in albums.folder, and the
folders are organised by format. Names match the folder names on Discogs.
If you add a folder on Discogs, add it here too (its id is printed in the
"Syncing folder ..." line of the database sync log).
"""
from typing import Optional

FOLDER_FORMATS = {
    2162484: "LP",
    2162488: "CD",
    2198943: "Digital",
    2162483: '7"',
    2162486: '10"',
    2198941: '12"',
    2162487: "Cassette",
    9628677: "DVD",
    2162485: "Autographed",
    1: "Uncategorized",
}


def format_for_folder(folder_id: Optional[int]) -> str:
    return FOLDER_FORMATS.get(folder_id, "Unknown")
