from typing import List, Optional

from starlette.requests import Request

from data.album import AlbumInfo
from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class PlayAlbumViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        folder = 2162484
        album_release_id, random_lp = RandomRecordService.get_folder_count2()
        print("Viewmodel album release id: ", album_release_id)

        release_data = RandomRecordService.get_album_data(album_release_id, random_lp)

        self.release_id = release_data.release_id
        self.release_url: Optional[str] = release_data.release_url
        self.artist_id = release_data.artist_id
        self.release_title: Optional[str] = release_data.release_title
        # self.artist_name: Optional[str] = release_data.artist_name
        # self.artist_url: Optional[str] = release_data.artist_url
        self.release_image_url: Optional[str] = release_data.release_image_url
        self.genres: Optional[List[str]] = release_data.genres
        # self.discogs_main_id: Optional[int] = release_data.discogs_main_id
        # self.discogs_main_url: Optional[str] = release_data.discogs_main_url
        self.album_release_date: Optional[str] = release_data.album_release_date
        # self.main_release_date: Optional[int] = release_data.main_release_date
