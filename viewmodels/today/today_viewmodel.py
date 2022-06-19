from starlette.requests import Request
from typing import List, Optional

from viewmodels.shared.viewmodel import ViewModelBase
from data.today_data import TodayInfo
from services import today_service, admin_service
import pendulum


class TodayViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # self.release_id: Optional[int] = None
        self.releases: List[TodayInfo] = []
        self.today_date = None

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in

        self.releases = await today_service.get_today_list()

        self.today_date = pendulum.now().format("MMMM Do")

        #        print("Vm.load: self.release_id: ", self.releases.release_id)

        return {}
