
from application.main.service.TrainingService import TrainingService
import csv
import json
import logging
import os

import pandas as pd
from application.main.service.AuthenticationService import (
    get_user_by_auth, token_authenticate, token_authenticate_admin)
from application.main.service.DocumentClassificationService import \
    DocumentClassificationService
from application.main.service.FileService import FileService
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('TRAINING_CONTROLLER',
                description='Training data operations')


@api.route('/')
@api.doc(security='Bearer Auth')
class TrainingDataController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        _parser = reqparse.RequestParser()
        self.training_service = TrainingService()
        _parser.add_argument("training_data", type=dict,
                             help='Training data is missing', required=True)
        self.req_parser = _parser
        super(TrainingDataController,
              self).__init__(*args, **kwargs)

    @api.doc(security='Bearer Auth')
    @token_authenticate
    def get(self):
        """DOWNLOAD TRAINING DATA"""
        try:
            user = get_user_by_auth()
            if(user):
                training_data = self.training_service.get_training_data(user)
                return training_data, 200
            else:
                responseObject = {
                    'status': 'Unauthorized',
                    'message': 'Unknown user'
                }
                return responseObject, 401
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'Internal Server Error',
                'message': 'Failed with internal error'
            }
            return responseObject, 500

    parser = None
    parser = api.parser()
    parser.add_argument('training_data', type=dict,
                        help='Document name is required')

    @api.doc(parser=parser, validate=True)
    @api.doc(security='Bearer Auth')
    @token_authenticate
    def post(self):
        """TRAIN MODEL"""
        args = self.req_parser.parse_args(strict=True)
        try:
            user = get_user_by_auth()
            if(user):
                self.training_service.train_model(
                    args.get('training_data'))
                return "Success", 200
            else:
                responseObject = {
                    'status': 'Unauthorized',
                    'message': 'Unknown user'
                }
                return responseObject, 401
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'Internal Server Error',
                'message': 'Failed with internal error'
            }
            return responseObject, 500
