from typing import List, Optional

from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase
from services.api_service import get_json_data as get_json


class APIJsonViewmodel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.image_url: str = ""
        self.artist: str = ""
        self.title: str = ""

    async def load(self) -> None:
        self.image_url = await get_json()
