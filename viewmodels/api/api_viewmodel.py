from typing import Optional, List
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import api_service


class DataViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.album: Optional[str] = None
        self.artist: Optional[str] = None
        self.image_url: Optional[str] = None

    async def load(self):
        self.album = await api_service.get_album_json()
        self.artist = await api_service.get_artist_json()
        self.image_url = await api_service.get_image_url_json()
