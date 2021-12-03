from typing import List

from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class AlbumChoiceViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        folder = 1
        album_release_id = 1026691

        self.folder = folder
        self.album_release_id = album_release_id

        self.album_type: str
        self.release_title: str = RandomRecordService.get_album_data(
            folder, album_release_id
        )
        self.release_uri: str = RandomRecordService.get_album_data(
            folder, album_release_id
        )
        self.artist_name: str = RandomRecordService.get_album_data(
            folder, album_release_id
        )
        self.release_title: str = RandomRecordService.get_album_data(
            folder, album_release_id
        )
