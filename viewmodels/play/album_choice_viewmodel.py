from typing import List

from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class AlbumChoiceViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.album_type: str
        self.release_title: str = RandomRecordService.get_album_data()
        self.release_uri: str = RandomRecordService.get_album_data()
        self.artist_name: str = RandomRecordService.get_album_data()
        self.release_title: str = RandomRecordService.get_album_data()
