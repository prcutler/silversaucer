from typing import Optional, List
from starlette.requests import Request
from data.release import Release

from services import admin_service
from services import play_service

from viewmodels.shared.viewmodel import ViewModelBase


class AdminViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_id: Optional[int] = None
        self.releases: List[Release] = []

        self.all_releases: List[Release] = []

        self.new_release_id: Optional[int] = None
        self.edit_release_id: Optional[int] = None

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in
        self.releases = await admin_service.missing_mb_info()

        self.all_releases = await play_service.get_album_list()

        form = await self.request.form()
        self.release_id = form.get("release_id")
        self.new_release_id = form.get("new_release_id")
        self.edit_release_id = form.get("edit_release_id")

        print("Vm.load: self.release_id: ", self.release_id)

        return {}
