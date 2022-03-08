import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/api/album")
def today():
    return {
        "album": "Like a Prayer",
        "artist": "Madonna",
        "url": "https://i.discogs.com/KiU4Bziov6339DcBKIvXaq9vYQQN9Gd95E39T3eIBmY/rs:fit/g:sm/q:90/h:600/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTQwNDQ0/OC0xNDU3MTk5ODMw/LTU4NzUuanBlZw.jpeg"
    }
