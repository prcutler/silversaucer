import fastapi
from fastapi_chameleon import template
from starlette.requests import Request, status

from services import user_service
from viewmodels.account.login_viewmodel import LoginViewModel

router = fastapi.APIRouter()


@router.get("/account/login")
@template(template_file="account/login.pt")
def login_get(request: Request):
    vm = LoginViewModel(request)
    return vm.to_dict()


@router.post("/account/login")
@template(template_file="account/login.pt")
async def login_post(request: Request):

    vm = LoginViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    user = user_service.login_user(vm.username, vm.password)
    if not user:
        vm.error = "You don't belong here.  Go away."
        return vm.to_dict()

    resp = fastapi.responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    return resp


@router.get("/account/logout")
def logout():
    response = fastapi.responses.RedirectResponse(
        url="/", status_code=status.HTTP_302_FOUND
    )

    return response
