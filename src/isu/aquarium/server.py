from __future__ import print_function
from pyramid.view import view_config
from pyramid.config import Configurator
from pkg_resources import resource_filename
import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize
from lxml import html
import os, os.path

morpher = pymorphy2.MorphAnalyzer()

SAVE_DIR=resource_filename("isu.aquarium","documents")

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

def get_body_data(request):
    body = request.body.decode("utf8")
    xml = html.fromstring(body)
    root = xml.xpath('//*[@id="main-document"]')[0]
    resource=root.get("resource", None)
    uuid=root.get("data-uuid", None)
    id=root.get("id", None)
    return body, resource

@view_config(route_name="api-save-as", renderer='json', request_method="POST")
def api_save_as(request):
    body, resource=get_body_data(request)
    return save_body(body, resource, overwite=False)

@view_config(route_name="api-save", renderer='json', request_method="POST")
def api_save(request):
    body, resource=get_body_data(request)
    return save_body(body, resource, overwite=True)

def save_body(body, resource, overwite):
    if resource is not None:
        if not os.path.isdir(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        filename=os.path.join(SAVE_DIR, resource+".xhtml")
        if not overwite and os.path.isfile(filename):
            return {"result": "ko", "error":"Document already exists!"}
        o=open(filename,"w")
        o.write(body)
        o.close()
        return {"result": "ok", "error":None}
    else:
        return {"result": "ko", "error":"Resource name is not found"}

def static_path(dir):
    return 'isu.aquarium:' + 'client/' + dir


def main(config, **settings):
    config = Configurator(settings=settings)
    config.add_route('document', '/')
    config.add_route('api-morphy', '/api/morphy')
    config.add_route('api-save', '/api/save')
    config.add_route('api-save-as', '/api/save-as')

    for asset in """assets css dist fonts images js""".split():
        config.add_static_view(name=asset, path=static_path(asset))

    config.scan()
    app = config.make_wsgi_app()
    return app
