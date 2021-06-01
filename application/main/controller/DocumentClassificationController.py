

import csv
import json
import logging
import os

import pandas as pd
from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin, get_user_by_auth)
from application.main.service.FileService import FileService
from application.main.service.DocumentClassificationService import DocumentClassificationService
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('DOCUMENT_CLASSIFICATION_CONTROLLER',
                description='Classification Operations')


@api.route('/download')
@api.doc(security='Bearer Auth')
class DownloadExtractionResultController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        _parser = reqparse.RequestParser()
        self.classification_service = DocumentClassificationService()
        _parser.add_argument("document_name", type=str,
                             help='File name', required=True)
        _parser.add_argument("document_id", type=int,
                             help='Document id', required=True)
        self.req_parser = _parser
        super(DownloadExtractionResultController,
              self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('document_name', type=str,
                        help='Document name is required')
    parser.add_argument('document_id', type=str,
                        help='Document ID is required')

    @api.doc(parser=parser, validate=True)
    @token_authenticate
    def get(self):
        """DOWNLOAD CLASSIFICATION RESULTS"""
        args = self.req_parser.parse_args(strict=True)
        user = get_user_by_auth()
        if(user):
            doc_name = args.document_name
            doc_id = args.document_id
            result = self.classification_service.get_all_paragraphs_and_tags_by_user(
                doc_name, doc_id, user)
            if(result):
                return result, 200
            else:
                extraction_results = []
                document_name = doc_name.document_name.split('.')[0]
                # filename = 'classified 2.csv'
                with open(os.path.join(current_app.config['RESULT_FOLDER'], document_name+".csv")) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0 or line_count == 1:
                            line_count += 1
                            continue
                        if row[0]:
                            tags = []
                            colIndex = 0
                            for col in row:
                                if(colIndex == 0):
                                    colIndex += 1
                                    continue
                                if(col):
                                    tags.append({'text': col})
                                colIndex += 1

                            extraction_results.append(
                                {'id': line_count, 'key': line_count, 'tag': tags, 'paragraph': row[0]})
                        line_count += 1
                    print(f'Processed {line_count} lines.')
                return extraction_results, 200
        else:
            responseObject = {
                'status': 'Unauthorized',
                'message': 'Unknown user'
            }
            return responseObject, 401


@api.route('/view-result')
@api.doc(security='Bearer Auth')
class ViewExtractionResultController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        self.classification_service = DocumentClassificationService()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        super(ViewExtractionResultController,
              self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('file_name', type=str, help='File name')

    @api.doc(parser=parser, validate=True)
    @token_authenticate_admin
    def get(self):
        """VIEW CLASSIFICATION RESULTS AS ADMIN"""
        args = self.req_parser.parse_args(strict=True)
        user = get_user_by_auth()
        if(user):
            # file_name=args.file_name
            file_name = 'CRPD.pdf'
            result = self.classification_service.get_all_paragraphs_and_tags(
                file_name)
            if(result):
                return result, 200
            else:
                responseObject = {
                    'status': 'Not found',
                    'message': 'Result not found'
                }
            return responseObject, 404
        else:
            responseObject = {
                'status': 'Unauthorized',
                'message': 'Unknown user'
            }
            return responseObject, 401


@api.route('/update', methods=['POST'])
@api.doc(security='Bearer Auth')
class UpdateClassificationResultController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.classification_service = DocumentClassificationService()
        self.file_service = FileService()
        parser = reqparse.RequestParser()
        parser.add_argument("document_name", type=str,
                            help='Document name is missing', required=True)
        parser.add_argument("edit",
                            type=dict, help='Incorrect request format',  required=True)
        self.req_parser = parser
        super(UpdateClassificationResultController,
              self).__init__(*args, **kwargs)

    @api.doc(security='Bearer Auth')
    @token_authenticate
    def post(self):
        """UPDATE CLASSIFICATION RESULT"""
        args = self.req_parser.parse_args(strict=True)
        try:
            edits = args.get('edit')
            document_name = args.get('document_name')
            user = get_user_by_auth()
            document = self.file_service.get_document(
                document_name, user)
            if(document):
                if edits:
                    classification_data = edits.get('classification_data')
                    training_data = edits.get('training_data')
                    table_edit_log = edits.get('table_edit_log')
                    # isClassificationSaved = edits.get('is_saved')
                    is_classification_saved = self.classification_service.is_document_classification(
                        document)
                    if(not is_classification_saved):
                        if(self.classification_service.save_classification_result(
                                document, classification_data)):

                            responseObject = {
                                'status': 'Success'
                            }
                            return responseObject, 200
                        else:
                            responseObject = {
                                'status': 'Data storing failed',
                                'message': 'Unknown error'
                            }
                        return responseObject, 500
                    else:
                        self.classification_service.update_classification_result(
                            user, document, table_edit_log)
                else:
                    responseObject = {
                        'status': 'Bad request',
                        'message': 'Invalid data'
                    }
                    return responseObject, 400
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
