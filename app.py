import os
from flask import Flask
from flask_restplus import Api, Resource

from flask import Blueprint, render_template


# Pywikibot
import pywikibot
from pywikibot import config2
# from pywikibot.data import api
# import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON

from flask_cors import CORS

# /Pywikibot

# from controller.FileController import api as file_ns
from main.controller.FileController import api as file_ns
# from main.controller.WikibaseController import api as wikibase_api_ns
from main.controller.WikibaseController import api as wikibase_api_ns
from main import create_app, db

# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy

blueprint = Blueprint('api', __name__, url_prefix="/api")
# blueprint = Blueprint('api', __name__)

# Authorization
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    },
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(blueprint,
          title='DISABILITY WIKI API DOCUMENT',
          version='1.0',
          description='Disability Open Linked Data Project ',
          security='Bearer Auth',
          authorizations=authorizations
          )
api.add_namespace(file_ns, path='/file')
api.add_namespace(wikibase_api_ns, path='/wikibase')


# BluePrint based regiter
# app = Flask(__name__)

# test = create_app('dev')
# print(test)

app = create_app('dev')
app.register_blueprint(blueprint)
db = SQLAlchemy(app)
app.app_context().push()


# Simple register
# api = Api(app)


# basic model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))


db.create_all()


def test_pywiki():
    family = 'my'
    mylang = 'my'
    familyfile = os.path.join(
        app.root_path.rsplit('\\', 1)[0], 'config', 'my_family.py')
    if not os.path.isfile(familyfile):
        print("family file %s is missing" % (familyfile))
    config2.register_family_file(family, familyfile)
    config2.password_file = app.root_path.rsplit(
        '\\', 1)[0]+'\\user-password.py'
    config2.usernames['my']['my'] = 'WikibaseAdmin'

    wikibase = pywikibot.Site("my", "my")
    wikibase_repo = wikibase.data_repository()
    print('connected')

    data = {}
    data['labels'] = {'en': 'TestITEM FROM FLASK',
                      'fr': 'item test france'}
    data['descriptions'] = {'en': 'TestITEM FROM FLASK'}
    new_item = pywikibot.ItemPage(wikibase_repo)
    new_item.editEntity(data)
    print(new_item.id)


# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}


@app.cli.command('debug')
def sim():
    app.run(debug=False)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
if __name__ == '__main__':
    app.run(debug=True)
