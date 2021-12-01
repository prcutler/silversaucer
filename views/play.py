import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/play_album")
@template(template_file="play/play_album.pt")
def play_album():
    return {}


@router.get("/play-single")
@template(template_file="play/play_single.pt")
def play_single():
    return {}
