from typing import List, Optional

from starlette.requests import Request

from services import choose_service, api_service
from data.album_data import Album

from viewmodels.shared.viewmodel import ViewModelBase


class ChooseResultsViewModel(ViewModelBase):
    def __init__(self, release_id, request: Request):
        super().__init__(request)

        self.release_id: int = release_id
        self.release_url: str = None
        self.artist_id: int = None
        self.artist_name: str = None
        self.release_title: str = None
        self.artist_url: str = None
        self.genres: List[str] = []
        self.release_image_url: Optional[str] = None
        self.album_release_year: Optional = None
        self.folder: int = None
        self.track_title: Optional[List](str) = None
        self.track_duration: Optional[List](str) = None
        self.track_position: Optional[List](str) = None
        self.track_info: Optional[List](str) = None
        self.mb_id: Optional[str] = None
        self.mb_release_date: Optional[str] = None

        self.login_status = self.is_logged_in

    async def load(self):

        release_data = await choose_service.get_release_data(self.release_id)
        print("release_data: ", release_data, release_data.release_id)
        print(release_data.genres, type(release_data.genres))

        self.release_id = release_data.release_id
        self.release_url = release_data.release_url
        self.artist_id = release_data.artist_id
        self.artist_url = release_data.artist_url
        self.genres = release_data.genres
        self.artist_name = release_data.artist_name
        self.release_title = release_data.release_title
        self.release_image_url = release_data.release_image_url
        self.album_release_year = release_data.album_release_year
        self.track_title: Optional[List](str) = release_data.track_title
        self.track_duration: Optional[List](str) = release_data.track_duration
        self.track_position: Optional[List](str) = release_data.track_position
        self.track_info: Optional[List](str) = release_data.track_info
        self.mb_id = release_data.mb_id
        self.mb_release_date = release_data.mb_release_date

        if self.login_status is False:
            print("False")
            pass
        else:
            print("Getting Album Art...")
            album_api_data = await api_service.update_api_db(
                self.release_title, self.artist_name, self.release_image_url
            )
            get_discogs_img = await api_service.get_discogs_image(
                self.release_image_url
            )
            publish_img = await api_service.publish_image()
