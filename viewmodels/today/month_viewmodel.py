from starlette.requests import Request
from typing import List, Optional

from viewmodels.shared.viewmodel import ViewModelBase
from data.today_data import TodayInfo
from services import today_service
import pendulum


class MonthViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        # self.release_id: Optional[int] = None
        self.releases: List[TodayInfo] = []
        self.month = None

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in

        self.releases = await today_service.get_month_list()

        self.month = pendulum.now(tz='America/Chicago').format("MMMM")

        #        print("Vm.load: self.release_id: ", self.releases.release_id)

        return {}
