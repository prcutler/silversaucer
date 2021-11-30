import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/play_album")
@template()
def play_albumy():
    return {}


@router.get("/play-single")
@template()
def play_single():
    return {}
