from typing import List, Optional

from starlette.requests import Request
from random import randint

from services import play_service, api_service
from viewmodels.shared.viewmodel import ViewModelBase


class PlaySingleViewModel(ViewModelBase):
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

        self.login_status = self.is_logged_in
        # print("Login status: ", self.login_status)

    async def load(self):

        random_folder = randint(1, 3)

        if random_folder == 1:
            folder = 2162486  # 10" folder
        elif random_folder == 2:
            folder = 2198941  # 12" folder
        else:
            folder = 2162483  # 7" folder

        release_data = await play_service.get_album_data(folder)
        # print("Release data: ", release_data)

        self.release_id = release_data.release_id
        self.release_url: Optional[str] = release_data.release_url
        self.artist_id = release_data.artist_id
        self.artist_url = release_data.artist_url
        self.artist_name = release_data.artist_name
        self.release_title: Optional[str] = release_data.release_title
        self.release_image_url: Optional[str] = release_data.release_image_url
        self.genres: Optional[List[str]] = release_data.genres
        self.album_release_date: Optional[str] = release_data.album_release_year
        self.main_release_date: Optional[str] = release_data.main_release_date
        self.track_title: Optional[List](str) = release_data.track_title
        self.track_duration: Optional[List](str) = release_data.track_duration
        self.track_position: Optional[List](str) = release_data.track_position


