

import csv
import json
import logging
import os

import pandas as pd
from application.main.service.AuthenticationService import (
    get_user_by_auth, token_authenticate, token_authenticate_admin)
from application.main.service.WikiEditRequestService import WikiEditRequestService
from flask import Flask, current_app, jsonify, request,  make_response
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('FILE_UPLOAD_REQUEST_CONTROLLER',
                description='Handle request of upload edits to Wikibase')


@api.route('/request_wiki_edit')
@api.doc(security='Bearer Auth')
class EditWikiRequestController(Resource):
    parser_ = None
    parser_ = api.parser()
    # parser_.add_argument('id[]', type=int, action='append')
    # request.args.getlist('id[]')
    parser_.add_argument('file_name', type=str,
                         help='File name')

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name is required', required=True)
        self.req_parser = parser
        self.edit_request_service = WikiEditRequestService()
        super(EditWikiRequestController, self).__init__(*args, **kwargs)

    @token_authenticate
    @api.doc(parser=parser_, validate=True)
    def get(self):
        args = self.req_parser.parse_args(strict=True)
        if(args.file_name):
            user = get_user_by_auth()
            """GET ALL FILE"""
            if(self.edit_request_service.create_upload_request(
                    args.file_name, user)):
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully created the request'
                }
                return responseObject, 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Document not found'
                }
                return responseObject, 400
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Document name is required'
            }
            return responseObject, 423
