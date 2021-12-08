from random import *

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from viewmodels.play.album_choice_viewmodel import AlbumChoiceViewModel
from viewmodels.play.choose_results_viewmodel import ChooseResultsViewModel
from viewmodels.play.now_playing_viewmodel import NowPlayingViewModel
from viewmodels.play.random_viewmodel import RandomViewModel

router = fastapi.APIRouter()


@router.get("/play/album-choice")
@template(template_file="play/album-choice.pt")
def album_choice(request: Request):
    vm = AlbumChoiceViewModel(request)


@router.post("/play/album-choice")
@template()
async def album_choice_post(request: Request):
    vm = AlbumChoiceViewModel(request)
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
        url="/play/now_playing", status_code=status.HTTP_302_FOUND
    )

    return resp

    # TODO - if empty, call random record service and redirect to now-playing


@router.get("/play/now-playing")
@template(template_file="play/now-playing.pt")
def now_playing(request: Request):
    vm = NowPlayingViewModel(request)

    return vm.to_dict()


@router.get("/play/now-playing/{album_release_id}")
@template(template_file="play/now-playing.pt")
def playing(release_id: int, request: Request):
    vm = RandomViewModel(release_id, request)

    return vm.to_dict()


@router.get("/play/play-single")
@template(template_file="play/play-single.pt")
def playsingle(request: Request):
    vm = NowPlayingViewModel(request)

    return vm.to_dict()
