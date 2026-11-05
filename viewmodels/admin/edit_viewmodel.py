import asyncio
from typing import List, Optional

import musicbrainzngs
from starlette.requests import Request
from services import admin_service
from infrastructure.mb_ids import RELEASE_GROUP, clean_date, parse_mb_id

from viewmodels.shared.viewmodel import ViewModelBase


class EditViewModel(ViewModelBase):
    def __init__(self, release_id, request: Request):
        super().__init__(request)

        self.release_data = []

        self.release_id: int = release_id
        self.release_url: Optional[str] = None
        self.artist_id: int = None
        self.artist_name: Optional[str] = None
        self.release_title: Optional[str] = None
        self.artist_url: Optional[str] = None
        self.release_image_url: Optional[str] = None
        self.album_release_year: Optional = None
        self.folder: int = None
        self.mb_id: Optional[str] = None
        self.mb_release_date: Optional[str] = None

        self.login_status = self.is_logged_in

    async def load(self):

        self.release_data = await admin_service.view_edit(self.release_id)
        # print("release_data: ", release_data, release_data.release_id)

        form = await self.request.form()

        self.release_id = self.release_data.release_id
        # self.release_url = release_data.release_url
        # self.artist_id = release_data.artist_id
        self.artist_name = form.get("artist_name")
        self.release_title = form.get("release_title")
        # self.artist_url = release_data.artist_url
        self.release_image_url = form.get("release_image_url")
        self.album_release_year = form.get("album_release_year")
        self.folder = form.get("folder")
        self.mb_id = form.get("mb_id")
        self.mb_release_date = form.get("mb_release_date")

        self.login_status = self.is_logged_in

        # return {}

    async def clean_musicbrainz_fields(self) -> None:
        """Reduce the pasted MusicBrainz ID to a bare release ID and tidy the
        date. Sets self.error if the ID can't be used."""
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
        self.mb_release_date = clean_date(self.mb_release_date)
