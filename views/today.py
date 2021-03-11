import fastapi
from fastapi_chameleon import template

router = fastapi.APIRouter()


@router.get("/today")
@template()
def today():
    return {}
