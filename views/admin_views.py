import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.admin.admin_viewmodel import AdminViewModel
from viewmodels.shared.viewmodel import ViewModelBase
from services import admin_service

router = fastapi.APIRouter()


@router.get("/admin/index")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await vm.load()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.get("/admin/")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await vm.load()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.get("/admin/create_db")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await vm.load()

    await admin_service.get_album_db_data()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.get("/admin/mb_data")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await admin_service.update_mb_id()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()

