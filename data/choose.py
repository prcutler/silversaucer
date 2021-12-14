class ChooseInfo:
    def __init__(
        self,
        folder: str,
        folder_number: int,
        release_title: str,
        artist_name: str,
        release_date: str,
        genres: str,
        main_release_date: int,
        album_release_date: str,
    ):

        self.artist_name = artist_name
        self.folder = folder
        self.folder_number = folder_number
        self.release_title = release_title
        self.artist_name = artist_name
        self.release_date = release_date
        self.genres = genres
        self.main_release_date: int = (main_release_date,)
        self.album_release_date = album_release_date
