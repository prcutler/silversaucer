from pyramid.view import view_config

from silversaucer.services.play_service import RandomRecordService


@view_config(route_name="play", renderer="silversaucer:templates/play/play.pt")
def play_album(_):

    album_release_id = RandomRecordService.get_lp_collection()
    # release_data = RandomRecordService.get_album_data(album_release_id)

    return {}


@view_config(
    route_name="play-single", renderer="silversaucer:templates/play/play-single.pt"
)
def play_single(_):
    return {}


@view_config(route_name="today", renderer="silversaucer:templates/today/today.pt")
def today(_):
    return {}
