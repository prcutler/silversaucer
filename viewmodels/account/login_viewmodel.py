from starlette.requests import Request

import data.config as config
from viewmodels.shared.viewmodel import ViewModelBase


class LoginViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.username = ""
        self.password = ""

    async def load(self):
        form = await self.request.form()
        self.username = form.get("username", "").lower().strip()
        print(self.username)
        self.password = form.get("password", "").strip()

        #        if not self.username():
        #            self.error = "You must specify a username."
        #        elif not self.password:
        #            self.error = "You must specify a password."
        if (
            not self.username == config.username
            and not self.password == config.password
        ):
            self.error = "You don't belong here.  Go away!"
