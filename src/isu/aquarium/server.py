from __future__ import print_function
from pyramid.view import view_config
from pyramid.config import Configurator
from pkg_resources import resource_filename


@view_config(route_name='document', renderer="isu.aquarium:templates/attorney.pt")
def document(request):
    return {}


@view_config(route_name="api-morphy", renderer='json', request_method="POST")
def api_morphy(request):
    return {"phrase": "Hello, You ...."}


def static_path(dir):
    return 'isu.aquarium:' + 'client/' + dir


def main(config, **settings):
    config = Configurator(settings=settings)
    config.add_route('document', '/')
    config.add_route('api-morphy', '/api/morphy')

    for asset in """assets css dist fonts images js""".split():
        config.add_static_view(name=asset, path=static_path(asset))

    config.scan()
    app = config.make_wsgi_app()
    return app
