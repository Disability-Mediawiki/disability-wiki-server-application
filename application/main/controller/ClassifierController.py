

import json
import logging
import os

from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin, get_user_by_auth)
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from application.main.service.FastTextService import FastTextService

api = Namespace('CLASSIFICATION_MODEL_CONTROLLER',
                description='MODEL OPERATIONS')


@api.route('/create')
# @api.doc(security='Bearer Auth')
class CreateModelController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        self.fast_text_service = FastTextService()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        super(CreateModelController,
              self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('file_name', type=str, help='File name')

    @api.doc(parser=parser, validate=True)
    def get(self):
        """CREATE CLASSIFICATION MODEL"""
        args = self.req_parser.parse_args(strict=True)
        file_name = args.file_name
        result = self.fast_text_service.create_model(file_name)
        # result = self.fast_text_service.classify_paragraph(file_name)
        if(result):
            return json.dumps({"resul": str(result)}), 200
        else:
            responseObject = {
                'status': 'Not found',
                'message': 'Result not found'
            }
        return responseObject, 404


@api.route('/classify')
# @api.doc(security='Bearer Auth')
class ClassifyTextController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        self.fast_text_service = FastTextService()
        parser.add_argument("text", type=str,
                            help='Text to classify', required=True)
        self.req_parser = parser
        super(ClassifyTextController,
              self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('text', type=str, help='File name')

    @api.doc(parser=parser, validate=True)
    def get(self):
        """CLASSIFY TEXT"""
        args = self.req_parser.parse_args(strict=True)
        text = args.text
        result = self.fast_text_service.classify_paragraph(text)
        if(result):
            return json.dumps({"resul": str(result)}), 200
        else:
            responseObject = {
                'status': 'Not found',
                'message': 'Result not found'
            }
        return responseObject, 404
