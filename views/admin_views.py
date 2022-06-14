import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.admin.admin_viewmodel import AdminViewModel
from viewmodels.admin.edit_viewmodel import EditViewModel
from viewmodels.shared.viewmodel import ViewModelBase
from services import admin_service

router = fastapi.APIRouter()


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


@router.get("/admin/index")
@template(template_file="admin/index.pt")
async def index(request: Request):
    vm = AdminViewModel(request)

    await vm.load()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.post("/admin/index", include_in_schema=False)
@template()
async def edit_post(request: Request):
    vm = AdminViewModel(request)
    await vm.load()

    episode_number = vm.release_id

    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/admin/edit-episode/{episode_number}", status_code=status.HTTP_302_FOUND
    )

    return response


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


@router.get("/admin/mb_date")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await admin_service.get_mb_date()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.get("/admin/edit")
@template(template_file="admin/edit-record.pt")
async def admin_edit(request: Request):
    vm = EditViewModel(request)

    await admin_service.edit_release(7663806)

   # return vm.to_dict()
    await vm.load()

    return vm.to_dict()
