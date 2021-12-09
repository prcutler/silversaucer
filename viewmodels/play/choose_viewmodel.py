from typing import List, Optional

from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class AlbumChooseViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # folder = 1
        # album_release_id = 1026691

        self.folder: Optional[str] = None
        self.folder_number: Optional[int] = None
        self.artist_name: Optional[str] = None
        self.release_title: Optional[str] = None
        self.release_date: Optional[int] = None
        self.genres: Optional[List[str]] = None
        self.main_release_date: Optional[int] = None

    async def load(self):
        form = await self.request.form()
        self.folder = form.get("folder")
        self.folder_number = form.get("folder_number")
        self.artist_name = form.get("artist_name")
        self.release_title = form.get("release_title")
        self.release_date = form.get("release_date")
        self.genres = form.getlist("genres")
        self.main_release_date = form.get("main_release_date")
