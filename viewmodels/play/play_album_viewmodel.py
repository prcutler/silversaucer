from typing import List, Optional

from starlette.requests import Request

import data.random_sayings
from services import api_service
from viewmodels.shared.viewmodel import ViewModelBase
from services import play_service


class PlayAlbumViewModel(ViewModelBase):
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
        self.random_saying = None
        self.login_status = self.is_logged_in
        print("Login status: ", self.login_status)

    async def load(self):
        # random_album_release_id = RandomRecordService.get_folder_count2(8)
        # release_data = RandomRecordService.get_album_data(random_album_release_id)

        release_data = await play_service.get_album_data(2162484)

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

        self.random_saying = data.random_sayings.get_random_saying()

        if self.login_status is False:
            print("False")
            pass
        else:
            album_api_data = await api_service.update_api_db(self.release_title,
                                                            self.artist_name, self.release_image_url)
            get_discogs_img = await api_service.get_discogs_image(self.release_image_url)
            publish_img = await api_service.publish_image(self.release_image_url)
#            total_count = await play_service.get_total_count()


