from typing import List, Optional

from starlette.requests import Request

import data.random_sayings
from data.album import AlbumInfo
from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class PlayAlbumViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        random_album_release_id = RandomRecordService.get_folder_count2(8)
        release_data = RandomRecordService.get_album_data(random_album_release_id)

        self.release_id = release_data.release_id
        self.release_url: Optional[str] = release_data.release_url
        self.artist_id = release_data.artist_id
        self.release_title: Optional[str] = release_data.release_title
        self.release_image_url: Optional[str] = release_data.release_image_url
        self.genres: Optional[List[str]] = release_data.genres
        self.album_release_date: Optional[str] = release_data.album_release_date
        self.track_title: Optional[List](str) = release_data.track_title
        self.track_duration: Optional[List](str) = release_data.track_duration
        self.track_position: Optional[List](str) = release_data.track_position
        self.random_saying: Optional[List](
            str
        ) = data.random_sayings.get_random_saying()
