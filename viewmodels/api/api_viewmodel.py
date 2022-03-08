from typing import List, Optional

from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase
from services import api_service


class APIJsonViewmodel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.image_url: str = ""
        self.artist: str = ""
        self.album: str = ""

    async def load(self) -> None:
        self.image_url = await api_service.get_image_url_json()
        self.artist = await api_service.get_artist_json()
        self.album = await api_service.get_album_json()
