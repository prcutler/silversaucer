from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class SoonViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        return {}
