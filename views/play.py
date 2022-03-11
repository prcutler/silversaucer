from random import *

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.play.choose_results_viewmodel import ChooseResultsViewModel
from viewmodels.play.choose_viewmodel import AlbumChooseViewModel
from viewmodels.play.play_album_viewmodel import PlayAlbumViewModel
from viewmodels.play.play_single_viewmodel import PlaySingleViewModel


router = fastapi.APIRouter()


@router.get("/play/choose")
@template(template_file="play/choose.pt")
def album_choice(request: Request):
    vm = AlbumChooseViewModel(request)
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

    # TODO: Write method for viewmodel to call service to get list choices
    # TODO - if empty, call random record service and redirect to now-playing

    resp = fastapi.responses.RedirectResponse(
        url="/play/choose-results", status_code=status.HTTP_302_FOUND
    )

    return resp


@router.get("/play/choose-results")
@template(template_file="play/choose-results.pt")
def album_choice(request: Request):
    vm = ChooseResultsViewModel(request)
    return vm.to_dict()


@router.post("play/choose-results")
@template()
async def album_choice_post(request: Request):
    vm = ChooseResultsViewModel(request)
    await vm.load()

    resp = fastapi.responses.RedirectResponse(
        url="/play/now-playing", status_code=status.HTTP_302_FOUND
    )

    return resp

    # TODO - if empty, call random record service and redirect to now-playing


@router.get("/play/play-album")
@template(template_file="play/play-album.pt")
async def now_playing(request: Request):
    vm = PlayAlbumViewModel(request)
    await vm.load()

    return vm.to_dict()


@router.get("/play/play-single")
@template(template_file="play/play-single.pt")
def play_single(request: Request):
    vm = PlaySingleViewModel(request)

    return vm.to_dict()
