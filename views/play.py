from random import *

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from services import choose_service

from viewmodels.play.choose_results_viewmodel import ChooseResultsViewModel
from viewmodels.play.choose_viewmodel import AlbumChooseViewModel
from viewmodels.play.play_album_viewmodel import PlayAlbumViewModel
from viewmodels.play.play_single_viewmodel import PlaySingleViewModel


router = fastapi.APIRouter()


@router.get("/play/choose")
@template(template_file="play/choose.pt")
async def album_choice(request: Request):
    vm = AlbumChooseViewModel(request)
    await vm.load()

    release_id = vm.release_id
    print("release_id viewmodel: ", release_id)

    return vm.to_dict()


@router.get("/play/soon")
@template(template_file="play/soon.pt")
def soon():

    return {}


@router.post("/play/choose")
@template()
async def album_choice_post(request: Request):
    vm = AlbumChooseViewModel(request)
    await vm.load()

    release_id = vm.release_id
    print("release_id viewmodel: ", release_id)
    # Redirect to Admin homepage on post
    response = fastapi.responses.RedirectResponse(
        url=f"/play/choose-results/{release_id}", status_code=status.HTTP_302_FOUND
    )

    return response


@router.get("/play/choose-results/{release_id}")
@template(template_file="play/choose-results.pt")
async def album_choice(release_id, request: Request):
    vm = ChooseResultsViewModel(release_id, request)

    await choose_service.get_release_data(release_id)

    await vm.load()

    return vm.to_dict()


@router.post("play/choose-results")
@template()
async def album_choice_post(request: Request):
    vm = ChooseResultsViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/play/play-album")
@template(template_file="play/play-album.pt")
async def now_playing(request: Request):
    vm = PlayAlbumViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/play/play-single")
@template(template_file="play/play-single.pt")
async def play_single(request: Request):
    vm = PlaySingleViewModel(request)

    await vm.load()

    return vm.to_dict()
