import fastapi
from fastapi_chameleon import template

from viewmodels.home.indexviewmodel import IndexViewModel
from viewmodels.shared.viewmodel import ViewModelBase

router = fastapi.APIRouter()


@router.get("/")
@template(template_file="")
def index():
    return


@router.get("/about")
@template(template_file="home/about.pt")
def about():
    return {}
