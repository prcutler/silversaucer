import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/")
@template(template_file="")
def index():
    return {}


@router.get("/about")
@template(template_file="home/about.pt")
def about():
    return {}
