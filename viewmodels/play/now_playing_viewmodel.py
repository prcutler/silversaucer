from typing import List, Optional

from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class NowPlayingViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        #        self.album_id = RandomRecordService.get_album_id
        #        self.album_info = RandomRecordService.get_album_info

        self.folder: Optional[str] = None
        self.folder_number: Optional[int] = None
        self.artist_name: Optional[str] = None
        self.release_title: Optional[str] = None
        self.release_date: Optional[int] = None
        self.genres: Optional[List[str]] = None
        self.main_release_date: Optional[int] = None
        self.album_id: Optional[str] = None
        self.release_uri: Optional[str] = None
        self.artist_url: Optional[str] = None
        self.release_image_uri: Optional[str] = None
        self.discogs_main_id: Optional[int] = None
        self.discogs_main_url: Optional[str] = None

        # if not self.album_id:
        #    return
