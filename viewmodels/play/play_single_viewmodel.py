from typing import List

from starlette.requests import Request

from services import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class PlaySingleViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_title: str = RandomRecordService.get_album_data()
        self.release_uri: str = RandomRecordService.get_album_data()
        self.artist_name: str = RandomRecordService.get_album_data()
        self.artist_url: str = RandomRecordService.get_album_data()
        self.release_image_uri: str = RandomRecordService.get_album_data()
        self.release_title: str = RandomRecordService.get_album_data()
        self.release_data: str = RandomRecordService.get_album_data()
        self.release_data: int = RandomRecordService.get_album_data()
        self.genres: str = RandomRecordService.get_album_data()
        self.discogs_main_id: int = RandomRecordService.get_album_data()
        self.discogs_main_url: str = RandomRecordService.get_album_data()
        self.main_release_date: int = RandomRecordService.get_album_data()
