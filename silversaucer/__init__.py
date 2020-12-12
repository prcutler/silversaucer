from pyramid.config import Configurator


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include("pyramid_chameleon")
    init_routing(config)
    return config.make_wsgi_app()


def init_routing(config):
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("play", "/play")
    config.add_route("play-single", "/play-single")
    config.add_route("today", "/today")
    config.add_route("about", "/about")
    config.scan()
