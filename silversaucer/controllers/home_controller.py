from pyramid.view import view_config


def get_test_packages():
    return [
        {'name': 'requests', 'version': '1.2.3'},
        {'name': 'sqlalchemy', 'version': '2.0.0'},
        {'name': 'pyramid', 'version': '1.7.7'},
    ]


@view_config(route_name='home', renderer='silversaucer:templates/home/index.pt')
def index(_):
    return {
        'packages': get_test_packages()
    }


@view_config(route_name='about', renderer='silversaucer:templates/home/about.pt')
def about(_):
    return {}


@view_config(route_name='play', renderer='silversaucer:templates/play/play.pt')
def play(_):
    return {}


@view_config(route_name='today', renderer='silversaucer:templates/today/today.pt')
def today(_):
    return {}