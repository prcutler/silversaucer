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

    #vm.album = "Heaven is a Place on Earth",
    #vm.artist = "Belinda Carlisle",
    #vm.image_url= "https://i.discogs.com/KiU4Bziov6339DcBKIvXaq9vYQQN9Gd95E39T3eIBmY/rs:fit/g:sm/q:90/h:600/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTQwNDQ0/OC0xNDU3MTk5ODMw/LTU4NzUuanBlZw.jpeg"

    album_data = {"album": vm.album, "artist": vm.artist, "image_url": vm.image_url}

    return album_data
#def json_get():
#    return {
#        "album": "Heaven is a Place on Earth",
#        "artist": "Belinda Carlisle",
#        "url": "https://i.discogs.com/KiU4Bziov6339DcBKIvXaq9vYQQN9Gd95E39T3eIBmY/rs:fit/g:sm/q:90/h:600/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTQwNDQ0/OC0xNDU3MTk5ODMw/LTU4NzUuanBlZw.jpeg"
#    }