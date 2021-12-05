class AlbumInfo:
    def __init__(
        self,
        album_id: int,
        release_title: str,
        release_uri: str,
        artist_name: str,
        artist_url: str,
        release_image_uri: str,
        release_date: str,
        genres: str,
        discogs_main_id: int,
        discogs_main_url: str,
        main_release_date: int,
    ):
        self.album_id = album_id
        self.release_title = release_title
        self.release_uri = release_uri
        self.artist_name = artist_name
        self.artist_url = artist_url
        self.release_image_uri = release_image_uri
        self.release_date = release_date
        self.genres = genres
        self.discogs_main_id: int = discogs_main_id
        self.discogs_main_url = discogs_main_url
        self.main_release_date: int = main_release_date
