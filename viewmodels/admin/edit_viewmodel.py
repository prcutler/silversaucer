from typing import List, Optional
from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class EditViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_id = None
        self.release_url = None
        self.artist_id = None
        self.artist_url = None
        self.artist_name = None
        self.release_title = None
        self.release_image_url = None
        self.genres = None
        self.album_release_date: Optional[str] = None
        self.main_release_date: Optional[str] = None
        self.track_title: Optional[List](str) = None
        self.track_duration: Optional[List](str) = None
        self.track_position: Optional[List](str) = None
        self.mb_id: Optional[str] = None

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in
        form = await self.request.form()

        return {}


