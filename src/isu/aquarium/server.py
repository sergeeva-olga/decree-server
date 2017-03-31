from __future__ import print_function
from pyramid.view import view_config
from pyramid.config import Configurator
from pkg_resources import resource_filename
import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize

morpher = pymorphy2.MorphAnalyzer()


@view_config(route_name='document',
             renderer="isu.aquarium:templates/attorney.pt")
def document(request):
    return {}


def lean(word, case):
    vals = morpher.parse(word)
    for v in vals:
        if 'NOUN' in v.tag:
            inflection = set(case.split())
            answer = v.inflect(inflection).word
            print(inflection, v, answer)
            return answer
    else:
        return ("<strong>Для слова {} не найден "
                "вариант существительного!</strong>".format(v))


@view_config(route_name="api-morphy", renderer='json', request_method="POST")
def api_morphy(request):
    query = request.json_body
    if query["all"]:
        words = simple_word_tokenize(query["phrase"])
        new_phrase = []
        for word in words:
            new_phrase.append(lean(word, case=query["case"]))
    return {"phrase": " ".join(new_phrase)}


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
