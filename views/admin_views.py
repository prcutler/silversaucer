import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.admin.admin_viewmodel import AdminViewModel
from viewmodels.admin.edit_viewmodel import EditViewModel
from viewmodels.admin.add_viewmodel import AddViewModel
from viewmodels.admin.add_record_data_viewmodel import AddRecordDataViewModel
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

    release_id = vm.release_id

    print("release_id viewmodel: ", release_id)
    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/admin/edit/{release_id}", status_code=status.HTTP_302_FOUND
    )

    return response


@router.post("/admin/", include_in_schema=False)
@template()
async def list_post(request: Request):
    vm = AdminViewModel(request)
    await vm.load()

    release_id = vm.release_id

    print("release_id viewmodel: ", release_id)

    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/admin/edit/{release_id}", status_code=status.HTTP_302_FOUND
    )

    return response


async def _start_import_job(request: Request, background_tasks, name: str, job):
    """Check login, then start an import job in the background.

    The job runs after the response is sent, so the page returns right away
    instead of waiting for (and timing out on) Discogs and MusicBrainz.
    """
    vm = AdminViewModel(request)
    await vm.load()

    if not vm.login_status:
        return fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )

    running = admin_service.job_in_progress()
    if running:
        vm.message = f"{running} is already running. Check back in a few minutes."
    else:
        background_tasks.add_task(admin_service.run_exclusive, name, job)
        vm.message = (
            f"{name} started in the background. It can take several minutes; "
            "progress is written to the server log."
        )

    return vm.to_dict()


@router.get("/admin/create_db")
@template(template_file="admin/index.pt")
async def create_db(request: Request, background_tasks: fastapi.BackgroundTasks):
    return await _start_import_job(
        request, background_tasks, "Database sync", admin_service.sync_collection
    )


@router.get("/admin/update_db")
@template(template_file="admin/index.pt")
async def update_db(request: Request, background_tasks: fastapi.BackgroundTasks):
    return await _start_import_job(
        request, background_tasks, "Database sync", admin_service.sync_collection
    )


@router.get("/admin/mb_date")
@template(template_file="admin/index.pt")
async def mb_date(request: Request, background_tasks: fastapi.BackgroundTasks):
    return await _start_import_job(
        request,
        background_tasks,
        "MusicBrainz date update",
        admin_service.get_mb_date,
    )


@router.get("/admin/edit/{release_id}")
@template(template_file="admin/edit-record.pt")
async def admin_edit(release_id, request: Request):
    vm = EditViewModel(release_id, request)
    print("admin view release_id: ", release_id)
    await admin_service.view_edit(release_id)

    await vm.load()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.post("/admin/edit/{release_id}", include_in_schema=False)
@template()
async def edit_post(release_id, request: Request):
    vm = EditViewModel(release_id, request)
    await vm.load()

    release_id = vm.release_id

    print("release_id viewmodel: ", release_id, "MB_ID: ", vm.mb_id)

    album = await admin_service.edit_release(
        release_id,
        vm.artist_name,
        vm.release_title,
        vm.release_image_url,
        vm.album_release_year,
        vm.folder,
        vm.mb_id,
        vm.mb_release_date,
    )

    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/admin/", status_code=status.HTTP_302_FOUND
    )

    return response


@router.get("/admin/add-release")
@template(template_file="admin/add-record.pt")
async def add_record(request: Request):
    vm = AddViewModel(request)

    await vm.load()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/admin/add-record-data", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.post("/admin/add-release", include_in_schema=False)
@template()
async def add_release_post(request: Request):
    vm = AdminViewModel(request)
    await vm.load()

    release_id = vm.release_id

    print("release_id viewmodel: ", release_id)
    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/admin/add-release/{release_id}", status_code=status.HTTP_302_FOUND
    )

    return response


@router.get("/admin/add-release/{release_id}")
@template(template_file="admin/add-record-data.pt")
async def add_record_data(release_id, request: Request):
    vm = AddRecordDataViewModel(release_id, request)

    await vm.load()

    if vm.login_status is False:
        response = fastapi.responses.RedirectResponse(
            url="/admin/add-record-data", status_code=status.HTTP_302_FOUND
        )
        return response
    else:
        return vm.to_dict()


@router.post("/admin/add-release/{release_id}", include_in_schema=False)
@template()
async def add_release_data_post(release_id, request: Request):
    vm = AddRecordDataViewModel(release_id, request)
    await vm.load()

    release_id = vm.release_id

    print("release_id viewmodel: ", release_id)

    await admin_service.add_new_release(release_id)

    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/admin/edit/{release_id}", status_code=status.HTTP_302_FOUND
    )

    return response
