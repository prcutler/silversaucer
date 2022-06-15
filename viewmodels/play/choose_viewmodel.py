from typing import List, Optional
from data.album_data import Album

from starlette.requests import Request

from services import play_service
from viewmodels.shared.viewmodel import ViewModelBase


class AlbumChooseViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_id: Optional[int] = None
        self.releases: List[Album] = []

        self.login_status = None

    async def load(self):
        self.login_status = self.is_logged_in
        self.releases = await play_service.get_album_list()

        form = await self.request.form()
        self.release_id = form.get("release_id")
        print("Vm.load: self.release_id: ", self.release_id)
