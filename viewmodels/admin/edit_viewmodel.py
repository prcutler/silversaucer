import asyncio
import datetime
import re
from typing import Optional

import musicbrainzngs
from starlette.requests import Request

from data.album_data import Album
from infrastructure.mb_ids import RELEASE_GROUP, clean_date, parse_mb_id
from services import admin_service
from viewmodels.shared.viewmodel import ViewModelBase

# Dates the Today/Month pages understand: 1991, 1991-04 or 1991-04-16.
_DATE_PATTERN = re.compile(r"\d{4}(-\d{2}(-\d{2})?)?")


def _clean_text(value: Optional[str]) -> Optional[str]:
    """Trim spaces; blank becomes None."""
    value = (value or "").strip()
    return value or None


def _valid_partial_date(value: str) -> bool:
    if not _DATE_PATTERN.fullmatch(value):
        return False
    parts = [int(p) for p in value.split("-")]
    year, month, day = parts + [1] * (3 - len(parts))
    try:
        datetime.date(year, month, day)
    except ValueError:  # month 13, April 31, ...
        return False
    return True


class EditViewModel(ViewModelBase):
    def __init__(self, release_id, request: Request):
        super().__init__(request)

        # The stored album; on a rejected save it shows the submitted values.
        self.release_data: Optional[Album] = None

        self.release_id = release_id
        self.artist_name: Optional[str] = None
        self.release_title: Optional[str] = None
        self.release_image_url: Optional[str] = None
        self.album_release_year: Optional[str] = None
        self.folder = None
        self.mb_id: Optional[str] = None
        self.mb_release_date: Optional[str] = None

        self.login_status = self.is_logged_in

    async def load(self):
        """Load the album, plus the submitted form values on a POST.

        release_data is None if there's no album with this release ID.
        """
        self.release_data = await admin_service.view_edit(self.release_id)
        if self.release_data is None:
            return

        self.release_id = self.release_data.release_id

        form = await self.request.form()
        self.artist_name = form.get("artist_name")
        self.release_title = form.get("release_title")
        self.release_image_url = form.get("release_image_url")
        self.album_release_year = form.get("album_release_year")
        self.folder = form.get("folder")
        self.mb_id = form.get("mb_id")
        self.mb_release_date = form.get("mb_release_date")

    async def validate(self) -> None:
        """Trim and check every submitted field, converting them to the values
        to store. Sets self.error (and stops) at the first problem."""
        self.artist_name = _clean_text(self.artist_name)
        self.release_title = _clean_text(self.release_title)
        self.release_image_url = _clean_text(self.release_image_url)
        self.album_release_year = _clean_text(self.album_release_year)
        self.mb_release_date = clean_date(self.mb_release_date)

        if not self.artist_name:
            self.error = "Artist can't be empty."
            return
        if not self.release_title:
            self.error = "Album can't be empty."
            return

        if self.album_release_year and not re.fullmatch(r"\d{4}", self.album_release_year):
            self.error = (
                f'Discogs release year "{self.album_release_year}" should be a '
                "four-digit year, like 1991, or left empty."
            )
            return

        folder = _clean_text(self.folder)
        if folder is None:
            self.folder = None
        elif folder.isdigit():
            self.folder = int(folder)
        else:
            self.error = (
                f'Folder "{folder}" should be a Discogs folder ID (a number, '
                "like 2162484 for LP)."
            )
            return

        if self.mb_release_date and not _valid_partial_date(self.mb_release_date):
            self.error = (
                f'MusicBrainz release date "{self.mb_release_date}" should look '
                "like 1991-04-16, or 1991-04 or 1991 if that's all that's known."
            )
            return

        await self.clean_musicbrainz_id()

    async def clean_musicbrainz_id(self) -> None:
        """Reduce the pasted MusicBrainz ID to a bare release ID.
        Sets self.error if the ID can't be used."""
        try:
            kind, mb_id = parse_mb_id(self.mb_id)
        except ValueError:
            self.error = (
                f"\"{self.mb_id.strip()}\" doesn't contain a MusicBrainz ID. Paste "
                "the release's ID or its musicbrainz.org/release/... address."
            )
            return

        if kind == RELEASE_GROUP:
            self.error = (
                "That's a release group (all editions of the album), not a "
                "release. Open it on MusicBrainz, pick the edition you own, and "
                "paste that release's address or ID."
            )
            return

        if mb_id:
            # Make sure it's a release, not an artist, track, release group...
            try:
                kind, name, _ = await asyncio.to_thread(
                    admin_service.identify_mb_entity, mb_id
                )
            except musicbrainzngs.WebServiceError as e:
                # MusicBrainz unreachable: save anyway rather than block edits.
                print("Could not verify MusicBrainz ID", mb_id, e)
                kind = "release"

            if kind is None:
                self.error = f"MusicBrainz has nothing with the ID {mb_id}."
                return
            if kind != "release":
                self.error = (
                    f"{mb_id} is a MusicBrainz {kind} (\"{name}\"), not a "
                    "release. Find the edition you own on MusicBrainz and paste "
                    "that release's address or ID."
                )
                return

        self.mb_id = mb_id

    def show_submitted_values(self) -> None:
        """Put what was typed back into the form, so a rejected save doesn't
        lose it. release_data is a detached copy, so this changes nothing in
        the database."""
        for field in (
            "artist_name",
            "release_title",
            "release_image_url",
            "album_release_year",
            "folder",
            "mb_id",
            "mb_release_date",
        ):
            setattr(self.release_data, field, getattr(self, field))
