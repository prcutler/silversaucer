from pyramid.view import view_config


@view_config(route_name='home', renderer='silversaucer:templates/home/index.pt')
def home_index(_):
    return {'project': 'silversaucer'}


@view_config(route_name='about', renderer='silversaucer:templates/home/about.pt')
def home_about(_):
    return {}
