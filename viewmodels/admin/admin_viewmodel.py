from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase
from services.play_service import RandomRecordService
from typing import Optional, List


class AdminViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

    async def load(self):
        form = await self.request.form()
        return {}


