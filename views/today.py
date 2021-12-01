import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/today")
@template(template_file="today/today.pt")
def today():
    return {}
