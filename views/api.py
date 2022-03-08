import fastapi
from fastapi_chameleon import template
from viewmodels.api.api_viewmodel import ApiViewModel

router = fastapi.APIRouter()


@router.get("/api/album")
async def json_data(request: Request):
    vm = ApiViewModel(request)
    await vm.load

    return vm.to_json()


