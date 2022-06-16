from typing import List, Optional
from starlette.requests import Request
from services import admin_service

from viewmodels.shared.viewmodel import ViewModelBase


class EditViewModel(ViewModelBase):
    def __init__(self, release_id, request: Request):
        super().__init__(request)

        self.release_id: int = release_id
        self.release_url: str = None
        self.artist_id: int = None
        self.artist_name: str = None
        self.release_title: str = None
        self.artist_url: str = None
        self.release_image_url: Optional[str] = None
        self.album_release_year: Optional = None
        self.folder: int = None
        self.mb_id: Optional[str] = None
        self.mb_release_date: Optional[str] = None

        self.login_status = self.is_logged_in

    async def load(self):

        release_data = await admin_service.edit_release(self.release_id)
        print("release_data: ", release_data, release_data.release_id)

        self.release_id = release_data.release_id
        self.release_url = release_data.release_url
        self.artist_id = release_data.artist_id
        self.artist_name = release_data.artist_name
        self.release_title = release_data.release_title
        self.artist_url = release_data.artist_url
        self.release_image_url = release_data.release_image_url
        self.album_release_year = release_data.album_release_year
        self.folder = release_data.folder
        self.mb_id = release_data.mb_id
        self.mb_release_date = release_data.mb_release_date

        self.login_status = self.is_logged_in

        # return {}


