from typing import List, Optional
from starlette.requests import Request
from services import admin_service

from viewmodels.shared.viewmodel import ViewModelBase


class AddViewModel(ViewModelBase):
    def __init__(self, release_id, request: Request):
        super().__init__(request)

        self.release_id: int = release_id

        self.login_status = self.is_logged_in

    async def load(self):

        form = await self.request.form()

        self.release_id = form.get("release_id")

        self.login_status = self.is_logged_in

        # return {}
