

from flask_restful import Resource, reqparse, reqparse
import os
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app

from application.main.service.AuthenticationService import token_authenticate
from application.main.service.UserService import UserService
from application.main.dto.UserDto import UserDto

# api = Namespace('USER_CONTROLLER', description='User controller')
api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserController(Resource):
    # method_decorators = ['token_required']

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.user_service = UserService()
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str,
                            help='User email', required=True)
        parser.add_argument("password", type=str,
                            help='Password', required=True)
        parser.add_argument("User name", type=str, help='User name')
        self.req_parser = parser

    def get(self):
        """GET USER"""
        auth_token = self.user_service.create_user()
        return "Hello from User" + auth_token

    @api.expect(_user, validate=True)
    def post(self):
        # The image is retrieved as a file
        args = self.req_parser.parse_args(strict=True)
        print(args)
        return "Some args"
