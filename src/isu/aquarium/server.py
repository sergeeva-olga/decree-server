from __future__ import print_function
from pyramid.view import view_config
from pyramid.config import Configurator


@view_config(route_name='hello', renderer='string')
def hello_world(request):
    return 'Hello World'


def main(config, **settings):
    config = Configurator(settings=settings)
    config.add_route('hello', '/')
    config.scan()
    app = config.make_wsgi_app()
    return app
