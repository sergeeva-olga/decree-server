from __future__ import print_function
from pyramid.view import view_config
from pyramid.config import Configurator


@view_config(route_name='hello', renderer='string')
def hello_world(request):
    return 'Hello World'


def static_path(dir):
    return 'isu.aquarium:' + 'client/' + dir


def main(config, **settings):
    config = Configurator(settings=settings)
    config.add_route('hello', '/')

    for asset in """assets css dist fonts images js""".split():
        config.add_static_view(name=asset, path=static_path(asset))

    config.scan()
    app = config.make_wsgi_app()
    return app
