from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase
from services.play_service import RandomRecordService
from typing import Optional, List


class AdminViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_id: [int] = None
        self.release_url: [str] = None
        self.artist_id: [str] = None
        self.artist_url: [str] = None
        self.artist_name: [str] = None
        self.release_title: [str] = None
        self.release_image_url: [str] = None
        self.genres: Optional[List](str) = None
        self.album_release_date: Optional[str] = None
        self.main_release_date: Optional[str] = None
        self.track_title: Optional[List](str) = None
        self.track_duration: Optional[List](str) = None
        self.track_position: Optional[List](str) = None

