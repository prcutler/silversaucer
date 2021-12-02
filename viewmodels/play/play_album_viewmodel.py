from typing import List

from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class PlayAlbumViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_uri: str
        self.release_image_uri: str
        self.release_title: str
        self.release_date: str
        self.release_date: str
        self.genres: str
