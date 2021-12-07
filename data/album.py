from typing import List


class AlbumInfo:
    def __init__(
        self,
        release_id,
        release_uri: str,
        artist_id: int,
        release_title: str,
        artist_name: str,
        artist_url: str,
        release_image_uri: str,
        genres: List[str],
        discogs_main_id: str,
        discogs_main_url: str,
        main_release_date: int,
        album_release_date: str,
    ):
        self.release_id = release_id
        self.release_uri = release_uri
        self.artist_id = artist_id
        self.release_title = release_title
        self.artist_name = artist_name
        self.artist_url = artist_url
        self.release_image_uri = release_image_uri
        self.genres = genres
        self.discogs_main_id: int = discogs_main_id
        self.discogs_main_url = discogs_main_url
        self.main_release_date: int = main_release_date
        self.album_release_date = album_release_date
