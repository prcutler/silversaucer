from typing import List, Optional

from starlette.requests import Request

from data.album import AlbumInfo
from services.play_service import RandomRecordService
from viewmodels.shared.viewmodel import ViewModelBase


class NowPlayingViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        folder = 2162484
        album_release_id = RandomRecordService.get_folder_count(folder)
        print(album_release_id)

        release_data = RandomRecordService.get_album_data(folder, album_release_id)

        self.folder = folder
        #      self.folder_number: Optional[int] = release_data.folder_number
        self.artist_name: Optional[str] = release_data.artist_name
        self.release_title: Optional[str] = release_data.release_title
        # self.release_date: Optional[int] = release_data.release_date
        self.main_release_date: Optional[int] = release_data.main_release_date
        self.album_id: Optional[str] = release_data.release_id
        self.artist_url: Optional[str] = release_data.artist_url
        # self.release_image_uri: Optional[str] = release_data.release_image_uri
        self.discogs_main_id: Optional[int] = release_data.discogs_main_id
        self.discogs_main_url: Optional[str] = release_data.discogs_main_url
        self.release_uri: Optional[str] = release_data.release_uri
        # self.genres: Optional[List[str]] = release_data.genres
