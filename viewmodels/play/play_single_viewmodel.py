from typing import List, Optional

from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class PlaySingleViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        get_random_folder = RandomRecordService.single_random_folder()
        # print(get_random_folder)
        random_album_release_id = RandomRecordService.get_folder_count2(
            get_random_folder
        )
        release_data = RandomRecordService.get_album_data(random_album_release_id)

        self.release_id = release_data.release_id
        self.release_url: Optional[str] = release_data.release_url
        self.artist_id = release_data.artist_id
        self.artist_url = release_data.artist_url
        self.artist_name = release_data.artist_name
        self.release_title: Optional[str] = release_data.release_title
        self.release_image_url: Optional[str] = release_data.release_image_url
        self.genres: Optional[List[str]] = release_data.genres
        self.album_release_date: Optional[str] = release_data.album_release_date
        self.main_release_date: Optional[str] = release_data.main_release_date
        self.track_title: Optional[List](str) = release_data.track_title
        self.track_duration: Optional[List](str) = release_data.track_duration
        self.track_position: Optional[List](str) = release_data.track_position
