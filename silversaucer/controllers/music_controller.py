from pyramid.view import view_config


@view_config(route_name='play', renderer='silversaucer:templates/play/play.pt')
def play(_):
    return {}


@view_config(route_name='today', renderer='silversaucer:templates/today/today.pt')
def today(_):
    return {}
