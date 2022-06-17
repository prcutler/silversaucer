from typing import Optional, List
from starlette.requests import Request
from data.release import Release

from services import admin_service

from viewmodels.shared.viewmodel import ViewModelBase


class AdminViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.release_id: Optional[int] = None
        self.releases: List[Release] = []

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in
        self.releases = await admin_service.missing_mb_info()

        form = await self.request.form()
        self.release_id = form.get("release_id")
        print("Vm.load: self.release_id: ", self.release_id)

        return {}


