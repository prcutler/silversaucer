import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.api.api_viewmodel import DataViewModel


router = fastapi.APIRouter()


@router.get("/album/data")
async def get_json(request: Request):
    vm = DataViewModel(request)
    await vm.load()

    album_data = {"album": vm.album, "artist": vm.artist, "image_url": vm.image_url}

    return album_data
