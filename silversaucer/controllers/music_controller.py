from random import *

from pyramid.request import Request
from pyramid.view import view_config

from silversaucer.services.play_service import RandomRecordService


@view_config(route_name="play", renderer="silversaucer:templates/play/play.pt")
def play(_):

    album_release_id = RandomRecordService.get_folder_count(2162484)
    print(album_release_id)
    release_data = RandomRecordService.get_album_data(album_release_id)
    print(release_data)

    return {"release_info": release_data}


@view_config(
    route_name="play-single", renderer="silversaucer:templates/play/play-single.pt"
)
def play_single(_):

    random_folder = randint(0, 2)
    if random_folder == 0:
        single = 2162483
    elif random_folder == 1:
        single = 2162486
    else:
        single = 2198941

    album_release_id = RandomRecordService.get_folder_count(single)
    print(album_release_id)
    release_data = RandomRecordService.get_album_data(album_release_id)

    return {"release_info": release_data}


@view_config(route_name="today", renderer="silversaucer:templates/today/today.pt")
def today(_):
    return {}
