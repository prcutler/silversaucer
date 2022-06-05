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
def admin_index(request: Request):
    vm = AdminViewModel(request)
    return vm.to_dict()


@router.get("/admin/")
@template(template_file="admin/index.pt")
def admin_index(request: Request):
    vm = AdminViewModel(request)
    return vm.to_dict()


@router.get("/admin/create_db")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await admin_service.get_album_db_data()

    return vm.to_dict()


@router.get("/admin/main_data")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await admin_service.get_main_release_data()

    return vm.to_dict()


@router.get("/admin/get_genres")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await admin_service.get_genre_data()

    return vm.to_dict()


@router.get("/admin/get_tracks")
@template(template_file="admin/index.pt")
async def admin_index(request: Request):
    vm = AdminViewModel(request)

    await admin_service.get_tracklist_data()

    return vm.to_dict()