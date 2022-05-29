import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.home.indexviewmodel import IndexViewModel
from viewmodels.shared.viewmodel import ViewModelBase

router = fastapi.APIRouter()


@router.get("/admin/index")
@template()
def admin_index(request: Request):
    vm = IndexViewModel(request)
    return vm.to_dict()


#@router.post("/home/index")
#@template()
#async def index(request: Request):
#    vm = IndexViewModel(request)
#    await vm.load

#    resp = fastapi.responses.RedirectResponse(
#        url="/play/now-playing", status_code=status.HTTP_302_FOUND
#    )


