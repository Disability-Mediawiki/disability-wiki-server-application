
from flask_restful import Resource,reqparse,reqparse
import os
from werkzeug import secure_filename,FileStorage,datastructures
from flask import request

class VideoController(Resource):
    def __init__(self):
        # Create a request parser
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, help='Name of the user', required=True)
        parser.add_argument("pass", type=str, help='Password of the user')
        self.req_parser = parser

    def put(self):
        # The image is retrieved as a file
        args = self.req_parser.parse_args(strict=True)
        print(args)
        return "Some args"

    def get(self):
        return "Hello from file"
