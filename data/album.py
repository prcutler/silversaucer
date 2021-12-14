from typing import List


class AlbumInfo:
    def __init__(
        self,
        release_id,
        release_url: str,
        artist_id: int,
        artist_name: str,
        release_title: str,
        artist_url: str,
        release_image_url: str,
        genres: List[str],
        # discogs_main_id: str,
        # discogs_main_url: str,
        main_release_date: int,
        album_release_date: str,
        track_title: str,
        track_duration: str,
        track_position: str,
    ):
        self.release_id = release_id
        self.release_url = release_url
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.release_title = release_title
        self.artist_url = artist_url
        self.release_image_url = release_image_url
        self.genres = genres
        # self.discogs_main_id: int = discogs_main_id
        # self.discogs_main_url = discogs_main_url
        self.main_release_date: int = main_release_date
        self.album_release_date = album_release_date
        self.track_title = track_title
        self.track_duration = track_duration
        self.track_position = track_position
