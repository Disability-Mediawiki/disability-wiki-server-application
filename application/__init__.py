import os
from flask import Flask
from flask_restplus import Api, Resource

from flask import Blueprint, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

from flask_bcrypt import Bcrypt

# from controller.FileController import api as file_ns
from application.main.controller.FileController import api as file_ns
# from main.controller.WikibaseController import api as wikibase_api_ns
from application.main.controller.WikibaseController import api as wikibase_api_ns
from application.main.controller.UserController import api as user_api_ns
from application.main.controller.EditWikiRequestController import api as request_wiki_edit_api_ns
from application.main.controller.GlssaryController import api as glossary_api_ns
from application.main import create_app, db

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
api.add_namespace(user_api_ns, path='/user')
api.add_namespace(request_wiki_edit_api_ns, path='/request')
api.add_namespace(glossary_api_ns, path='/glossary')


# app = create_app('dev')
# CORS(app, resources={r'/*': {'origins': '*'}})
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# app.register_blueprint(blueprint)


# moved from manage.py
# app.app_context().push()
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
