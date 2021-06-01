

from application.main.service.FileService import FileService
from application.main.service.DocumentClassificationService import DocumentClassificationService
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


@api.route('/upload-wikiedit', methods=['POST'])
@api.doc(security='Bearer Auth')
class UploadWikieditRequestController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.edit_request_service = WikiEditRequestService()
        self.file_service = FileService()
        parser = reqparse.RequestParser()
        parser.add_argument("document", type=dict,
                            help='Document name is missing', required=True)
        self.req_parser = parser
        super(UploadWikieditRequestController,
              self).__init__(*args, **kwargs)

    @api.doc(security='Bearer Auth')
    @token_authenticate
    def post(self):
        """UPLOAD WIKIEDIT REQUEST """
        args = self.req_parser.parse_args(strict=True)
        # args = request.data
        try:
            document_payload = args.get('document')
            user = get_user_by_auth()
            document = self.file_service.get_document(
                document_payload.get('name'), user)
            if(document):
                if(self.edit_request_service.create_wikiedit_upload_request(
                        user, document)):
                    responseObject = {
                        'status': 'Success',
                        'message': 'Upload request created'
                    }
                return responseObject, 200
            else:
                responseObject = {
                    'status': 'Not Found',
                    'message': 'Document not found'
                }
                return responseObject, 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'Internal Server Error',
                'message': 'Failed with internal error'
            }
            return responseObject, 500


@api.route('/get-pending-request', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetPendingWikieditRequestController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.edit_request_service = WikiEditRequestService()
        self.file_service = FileService()
        super(GetPendingWikieditRequestController,
              self).__init__(*args, **kwargs)

    @api.doc(security='Bearer Auth')
    @token_authenticate_admin
    def get(self):
        """GET ALL PENDING WIKIEDIT REQUEST"""

        try:
            ""
            result = self.edit_request_service.get_all_pending_request()
            return jsonify(result)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'Internal Server Error',
                'message': 'Failed with internal error'
            }
            return responseObject, 500


@api.route('/request-verify', methods=['GET'])
@api.doc(security='Bearer Auth')
class VerifyWikiEditRequestController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.edit_request_service = WikiEditRequestService()
        self.file_service = FileService()
        parser = reqparse.RequestParser()
        parser.add_argument("request_id", type=str,
                            help='Data is missing', required=True)
        parser.add_argument("document_id", type=str,
                            help='Data is missing', required=True)
        parser.add_argument("status", type=str,
                            help='Data is missing', required=True)
        self.req_parser = parser
        super(VerifyWikiEditRequestController,
              self).__init__(*args, **kwargs)

    @api.doc(security='Bearer Auth')
    @token_authenticate_admin
    def get(self):
        """UPDATE ACTION ON WIKI-EDIT REQUEST"""
        args = self.req_parser.parse_args(strict=True)
        request_id = args.get('request_id')
        document_id = args.get('document_id')
        status = args.get('status')

        try:
            document = self.file_service.get_document_by_id(
                document_id)
            if(document):
                result = self.edit_request_service.update_wikiedit_request(
                    document, request_id, status)
                if(result):
                    responseObject = {
                        'status': 'Action successfully updated',
                        'message': 'Updated successfully'
                    }
                    return jsonify(result)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'Internal Server Error',
                'message': 'Failed with internal error'
            }
            return responseObject, 500
