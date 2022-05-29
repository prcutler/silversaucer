from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase
from services.play_service import RandomRecordService
from typing import Optional, List


class AdminViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_id = None
        self.release_url = None
        self.artist_id = None
        self.artist_url = None
        self.artist_name = None
        self.release_title = None
        self.release_image_url = None
        self.genres = None
        self.album_release_date: Optional[str] = None
        self.main_release_date: Optional[str] = None
        self.track_title: Optional[List](str) = None
        self.track_duration: Optional[List](str) = None
        self.track_position: Optional[List](str) = None


    async def load(self):
        random_album_release_id = RandomRecordService.get_folder_count2(8)
        release_data = RandomRecordService.get_album_data(random_album_release_id)

        self.release_id = release_data.release_id
        self.release_url = release_data.release_url
        self.artist_id = release_data.artist_id
        self.artist_url = release_data.artist_url
        self.artist_name = release_data.artist_name
        self.release_title: Optional[str] = release_data.release_title
        self.release_image_url = release_data.release_image_url
        self.genres = release_data.genres
        self.album_release_date: Optional[str] = release_data.album_release_date
        self.main_release_date: Optional[str] = release_data.main_release_date
        self.track_title: Optional[List](str) = release_data.track_title
        self.track_duration: Optional[List](str) = release_data.track_duration
        self.track_position: Optional[List](str) = release_data.track_position