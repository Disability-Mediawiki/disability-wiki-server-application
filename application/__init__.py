
import os
from flask import Flask
from flask_restplus import Api, Resource

from flask import Blueprint, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

from flask_bcrypt import Bcrypt

from application.main.controller.FileController import api as file_ns
from application.main.controller.WikibaseController import api as wikibase_api_ns
from application.main.controller.UserController import api as user_api_ns
from application.main.controller.UploadRequestController import api as upload_request_api_ns
from application.main.controller.GlossaryController import api as glossary_api_ns
from application.main.controller.DocumentClassificationController import api as classification_api_ns
from application.main.controller.TrainingDataController import api as training_api_ns
from application.main.controller.WebContentController import api as web_content_api_ns
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
api.add_namespace(upload_request_api_ns, path='/request')
api.add_namespace(glossary_api_ns, path='/glossary')
api.add_namespace(classification_api_ns, path='/doc-classifiy')
api.add_namespace(training_api_ns, path='/training')
api.add_namespace(web_content_api_ns, path='/web-content')
