from typing import List


class TodayInfo:
    def __init__(
        self,
        release_id,
        release_url: str,
        artist_id: int,
        artist_name: str,
        release_title: str,
        artist_url: str,
        release_image_url: str,
        album_release_year: str,
        mb_id: str,
        mb_release_date: str,
    ):
        self.release_id = release_id
        self.release_url = release_url
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.release_title = release_title
        self.artist_url = artist_url
        self.release_image_url = release_image_url
        self.album_release_year = album_release_year
        self.mb_id = mb_id
        self.mb_release_date = mb_release_date
