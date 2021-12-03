from typing import List

from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class NowPlayingViewModel(ViewModelBase):
    def __init__(self, album_id: int, request: Request):
        super().__init__(request)

        self.album_id = RandomRecordService.get_album_id
        self.album_info = RandomRecordService.get_album_info

        if not self.album_id:
            return
