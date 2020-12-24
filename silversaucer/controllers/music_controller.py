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

    album_release_id = RandomRecordService.get_folder_count(2162484)
    print(album_release_id)
    # release_data = RandomRecordService.get_album_data(album_release_id)

    return {}


@view_config(route_name="today", renderer="silversaucer:templates/today/today.pt")
def today(_):
    return {}
