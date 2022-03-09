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
        self.artist = "Artist"
        self.image_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
