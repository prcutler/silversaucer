from starlette.requests import Request
from typing import List, Optional

from viewmodels.shared.viewmodel import ViewModelBase
from data.today_data import TodayInfo
from services import today_service
import pendulum


class MonthViewModel(ViewModelBase):
    def __init__(self, request: Request, offset: int = 0):
        super().__init__(request)

        # self.release_id: Optional[int] = None
        self.releases: List[TodayInfo] = []
        self.month = None

        self.offset = offset
        self.prev_offset = offset - 1
        self.next_offset = offset + 1

        self.login_status = None

    async def load(self):

        self.login_status = self.is_logged_in

        self.releases = await today_service.get_month_list(self.offset)

        target_date = pendulum.now(tz='America/Chicago').add(months=self.offset)
        self.month = target_date.format("MMMM")

        #        print("Vm.load: self.release_id: ", self.releases.release_id)

        return {}
