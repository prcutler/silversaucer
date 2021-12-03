from typing import List, Optional

from starlette.requests import Request

from services import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class AlbumChoiceViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # folder = 1
        # album_release_id = 1026691

        self.folder: Optional[str] = None
        self.folder_number: Optional[int] = None
        self.artist_name: Optional[str] = None
        self.release_title: Optional[str] = None
        self.release_date: Optional[int] = None
        self.genres: Optional[List[str]] = None
        self.main_release_date: Optional[int] = None
