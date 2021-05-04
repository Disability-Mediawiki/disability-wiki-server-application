

from flask_restful import Resource, reqparse, reqparse
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app

from application.main.model.User import User
from .. import db, flask_bcrypt
api = Namespace('USER_CONTROLLER', description='User controller')


@api.route('/')
class UserService():
    def __init__(self):
        "sdf"

    def create_user(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        return auth_token
