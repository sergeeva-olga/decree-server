from __future__ import print_function
from pyramid.view import view_config
from pyramid.config import Configurator
from pkg_resources import resource_filename
import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize
from lxml import html
from lxml import etree
import os, os.path
import rdflib
from pyramid.renderers import render

morpher = pymorphy2.MorphAnalyzer()
BASE_URL= "http://irnok.net:8080/" # + UUID + ".xhtml"

def asBaseURL(uuid):
    return BASE_URL+uuid+".xhtml"

SAVE_DIR=resource_filename("isu.aquarium","documents")

class DocumentData(object):
    def __init__(self, request):
        if hasattr(request, "matchdict"):
            if "document_uuid" in request.matchdict:
                return self.load(uuid=request.matchdict["document_uuid"])
        return self.get_body_data(request)

    def load(self, uuid):
        i = open(self.filename(uuid), "r")
        self.body = i.read()
        i.close()

    def get_body_data(self, request):
        self.body = request.body.decode("utf8")
        self.xml = html.fromstring(self.body)
        root = self.root = self.xml.xpath('//*[@id="main-document"]')[0]
        self.resource=root.get("resource", None)
        self.uuid=root.get("data-uuid", None)
        self.id=root.get("id", None)

    def filename(self, uuid=None):
        if uuid is None:
            uuid=self.uuid
        if not os.path.isdir(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        return os.path.join(SAVE_DIR, uuid+".xhtml")


    def save_body(self, overwite):
        if self.resource is not None:
            filename = self.filename()
            if not overwite and os.path.isfile(filename):
                return {"result": "KO", "error":"Document already exists!"}
            # Ok, we must save the content
            o=open(filename,"w")
            o.write(self.body)
            o.close()
            self.index()
            return {"result": "OK", "error":"Document successfully saved!"}
        else:
            return {"result": "KO", "error":"Resource name is not found!"}

    def index(self):
        url= asBaseURL(self.uuid)
        txt = etree.tostring(self.xml, encoding=str, pretty_print=True)
        result = render("isu.aquarium:templates/editor.pt", {"content":txt})
        print(result)
        g=rdflib.Graph()
        g.parse(data=result, publicID=url, format='rdfa')
        print(len(g))

@view_config(route_name='document',
             renderer="isu.aquarium:templates/editor.pt")
def document(request):
    doc = DocumentData(request)
    return {"content":doc.body}


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


@view_config(route_name="api-save-as", renderer='json', request_method="POST")
def api_save_as(request):
    doc = DocumentData(request)
    return doc.save_body(overwite=False)

@view_config(route_name="api-save", renderer='json', request_method="POST")
def api_save(request):
    doc = DocumentData(request)
    return doc.save_body(overwite=True)

def static_path(dir):
    return 'isu.aquarium:' + 'client/' + dir


def main(config, **settings):
    config = Configurator(settings=settings)
    config.add_route('document', '/{document_uuid}.xhtml')
    config.add_route('api-morphy', '/api/morphy')
    config.add_route('api-save', '/api/save')
    config.add_route('api-save-as', '/api/save-as')

    for asset in """assets css dist fonts images js""".split():
        config.add_static_view(name=asset, path=static_path(asset))

    config.scan()
    app = config.make_wsgi_app()
    return app
