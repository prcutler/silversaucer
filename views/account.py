import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from infrastructure import cookie_auth
from services import user_service
from viewmodels.account.account_viewmodel import AccountViewModel
from viewmodels.account.login_viewmodel import LoginViewModel

router = fastapi.APIRouter()


@router.get("/account")
@template()
def index(request: Request):
    vm = AccountViewModel(request)
    return vm.to_dict()


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

    resp = fastapi.responses.RedirectResponse(
        "/account", status_code=status.HTTP_302_FOUND
    )
    cookie_auth.set_auth(resp, user.id)

    return resp


@router.get("/account/logout")
def logout():
    response = fastapi.responses.RedirectResponse(
        url="/", status_code=status.HTTP_302_FOUND
    )
    cookie_auth.logout(response)

    return response
