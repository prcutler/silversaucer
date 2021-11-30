import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/")
@template()
def index():
    return {}


@router.get("/about")
@template()
def about():
    return {}
