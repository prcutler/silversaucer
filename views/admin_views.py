import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.admin.admin_viewmodel import AdminViewModel
from viewmodels.shared.viewmodel import ViewModelBase

router = fastapi.APIRouter()


@router.get("/admin/index")
@template(template_file="admin/index.pt")
def admin_index(request: Request):
    vm = AdminViewModel(request)
    return vm.to_dict()




