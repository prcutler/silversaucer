import fastapi
from fastapi_chameleon import template
from starlette.requests import Request
from viewmodels.today.today_viewmodel import TodayViewModel


router = fastapi.APIRouter()


@router.get("/today")
@template(template_file="today/today.pt")
async def today(request: Request):
    vm = TodayViewModel(request)
    await vm.load()
