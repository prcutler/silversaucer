from typing import List, Optional
from starlette.requests import Request
from services import admin_service

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
