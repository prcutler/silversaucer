from viewmodels.shared.viewmodel import ViewModelBase


class LoginViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.username = ""
        self.password = ""

    async def load(self):
        form = await self.request.form()
        self.username = form.get("username", "").lower().strip()
        self.password = form.get("password", "").strip()

        if not self.username or not self.email.strip():
            self.error = "You must specify a username."
        elif not self.password:
            self.error = "You must specify a password."
