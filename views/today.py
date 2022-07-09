import fastapi
from fastapi_chameleon import template
from starlette.requests import Request
from viewmodels.today.today_viewmodel import TodayViewModel
from viewmodels.today.month_viewmodel import MonthViewModel


router = fastapi.APIRouter()


@router.get("/today")
@template(template_file="today/today.pt")
async def today(request: Request):
    vm = TodayViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/month")
@template(template_file="today/month.pt")
async def month(request: Request):
    vm = MonthViewModel(request)
    await vm.load()

    return vm.to_dict()
