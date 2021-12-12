from typing import List, Optional

from starlette.requests import Request

from services.choose_service import ChooseService
from viewmodels.shared.viewmodel import ViewModelBase


class AlbumChooseViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.folder_id = ChooseService.get_folder_id_list()
        self.folder_number = ChooseService.get_folder_id_list()
        self.artist_name: ChooseService.get_artist_name()
        self.release_title = ChooseService.get_album_names()
        self.album_id = ChooseService.get_album_id()
        self.release_date: Optional[int] = None
        self.genres: Optional[List[str]] = None
        # self.main_release_date: Optional[int] = None

    async def load(self):
        form = await self.request.form()
        self.folder = form.get("folder_id")
        self.folder_number = form.get("folder_number")
        self.artist_name = form.get("artist_name")
        self.release_title = form.get("release_title")
        self.album_id = form.get("album_id")
        self.release_date = form.get("release_date")
        self.genres = form.getlist("genres")
        # self.main_release_date = form.get("main_release_date")
