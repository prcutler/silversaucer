from typing import List

from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class PlayAlbumViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)
