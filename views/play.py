import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/play")
@template()
def play():
    return {}


@router.get("/play-single")
@template()
def play_single():
    return {}
