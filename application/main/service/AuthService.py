
import logging
import os

from application.main.model.User import BlacklistToken, User
from application.main.service.SparqlService import SparqlService
from application.main.service.WikibaseApi import WikibaseApi
from flask import current_app
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from .. import db
from .. import flask_bcrypt


class AuthService():
    def __init__(self):
        self.wikibase_api = WikibaseApi()
        self.sparql_service = SparqlService()

    def validate_password(self, user_password, password):
        return flask_bcrypt.check_password_hash(
            user_password, password
        )

    def blacklist_token(self, token):
        try:
            blacklist_token = BlacklistToken(token=token)
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            return blacklist_token
        except Exception as e:
            print(e)
            db.session.rollback()
            raise
