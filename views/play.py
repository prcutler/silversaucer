from random import *

import fastapi
from fastapi_chameleon import template
from starlette.requests import Request

from services.play_service import RandomRecordService
from viewmodels.play.play_album_viewmodel import PlayAlbumViewModel
from viewmodels.play.play_single_viewmodel import PlaySingleViewModel
from viewmodels.play.play_viewmodel import PlayViewModel
from viewmodels.shared.viewmodel import ViewModelBase

router = fastapi.APIRouter()


@router.get("/play")
@template(template_file="play/play.pt")
def play(request: Request):
    vm = PlayViewModel(request)
    return {vm.to_dict}


@router.get("/play/{album_id}")
@template(template_file="play/play-album.pt")
def play_album(request: Request):
    vm = PlayViewModel(request)
    folder = 2162484
    album_release_id = RandomRecordService.get_folder_count(folder)
    release_data = RandomRecordService.get_album_data(folder, album_release_id)
    return {vm.to_dict}


@router.get("single-{album_id}")
@template(template_file="play/play_single.pt")
def play_single(request: Request):
    vm = PlayViewModel(request)
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

    return {vm.to_dict}
