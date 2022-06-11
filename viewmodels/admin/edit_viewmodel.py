from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class EditViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in
        form = await self.request.form()

        return {}


