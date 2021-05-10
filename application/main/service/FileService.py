

from flask_restful import Resource, reqparse, reqparse
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import Flask, request, jsonify, current_app
from flask_restplus import Resource, Api, Namespace
from flask import current_app

from application.main.model.User import User
from .. import db, flask_bcrypt

from application.main.service.WikibaseApi import WikibaseApi
from application.main.service.AuthService import AuthService


class FileService():
    def __init__(self):
        self.auth_service = AuthService()

    def move_file_wiki_upload_request(self, file_name):
        try:
            if os.path.isfile(os.path.join(
                    current_app.config['RESULT_FOLDER'], file_name)):
                os.replace(os.path.join(
                    current_app.config['RESULT_FOLDER'], file_name),
                    os.path.join(
                    current_app.config['UPLOAD_WIKIEDIT_REQUEST_FOLDER'], file_name))
                return True
            else:
                return False
        except IOError:
            file.close()
            print("File not accessible")
            return False
        # os.rename("path/to/current/file.foo",
        #           "path/to/new/destination/for/file.foo")
        # shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
        # os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
