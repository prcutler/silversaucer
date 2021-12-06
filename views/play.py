from random import *

import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.play.album_choice_viewmodel import AlbumChoiceViewModel
from viewmodels.play.choose_results_viewmodel import ChooseResultsViewModel
from viewmodels.play.now_playing_viewmodel import NowPlayingViewModel
from viewmodels.shared.viewmodel import ViewModelBase

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

    album = RandomRecordService.get_random_album(
        vm.artist_name,
        vm.folder,
        vm.folder_number,
        vm.genres,
        vm.release_date,
        vm.release_title,
        vm.main_release_date,
    )
    resp = fastapi.responses.RedirectResponse(
        url="/play/choose-results", status_code=status.HTTP_302_FOUND
    )

    return resp

    # TODO - if empty, call random record service and redirect to now-playing


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

    album = RandomRecordService.get_random_album(
        vm.artist_name,
        vm.folder,
        vm.folder_number,
        vm.genres,
        vm.release_date,
        vm.release_title,
        vm.main_release_date,
    )
    resp = fastapi.responses.RedirectResponse(
        url="/play/now_playing", status_code=status.HTTP_302_FOUND
    )

    return resp

    # TODO - if empty, call random record service and redirect to now-playing


@router.get("/play/now-playing")
@template(template_file="play/now-playing.pt")
def now_playing(request: Request):
    vm = NowPlayingViewModel(request)

    folder = 2162484
    album_release_id = RandomRecordService.get_folder_count(folder)
    print(album_release_id)

    release_data = RandomRecordService.get_album_data(folder, album_release_id)
    return vm.to_dict()


@router.get("/play/play-single")
@template(template_file="play/play-single.pt")
def playsingle(request: Request):
    vm = NowPlayingViewModel(request)
    random_folder = randint(0, 2)
    if random_folder == 0:
        single = 2162483
    elif random_folder == 1:
        single = 2162486
    else:
        single = 2198941

    folder = single

    album_release_id = RandomRecordService.get_folder_count(single)
    release_data = RandomRecordService.get_album_data(folder, album_release_id)
    return vm.to_dict()
