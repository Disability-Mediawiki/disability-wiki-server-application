

import csv
import json
import logging
import os

import pandas as pd
from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin, get_user_by_auth)
from application.main.service.FileService import FileService
from application.main.service.PdfService import PdfService
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('FILE_CONTROLLER', description='File operations')


@api.route('/download')
@api.doc(security='Bearer Auth')
class DownloadExtractionController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        super(DownloadExtractionController, self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('file_name', type=str, help='File name')

    @api.doc(parser=parser, validate=True)
    def get(self):
        args = self.req_parser.parse_args(strict=True)
        """DOWNLOAD CLASSIFICATION RESULTS"""
        extraction_results = []
        with open(os.path.join(current_app.config['RESULT_FOLDER'], args.file_name)) as csv_file:
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


@api.route('/get-all-document', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetDocumentListController(Resource):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        super(GetDocumentListController, self).__init__(*args, **kwargs)

    def obj_dict(self, obj):
        return obj.__dict__

    def get(self):
        """GET ALL DOCUMENTS"""
        try:
            user = get_user_by_auth()
            if(user):
                document_list = self.file_service.get_all_document(user)
                return jsonify(document_list)
            else:
                return "invalid token", 403
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/get-pending-document', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetPendingDocumentListController(Resource):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        super(GetPendingDocumentListController, self).__init__(*args, **kwargs)

    def get(self):
        """GET ALL PENDING DOCUMENTS"""
        try:
            user = get_user_by_auth()
            if(user):
                document_list = self.file_service.get_all_pending_document(
                    user)
                return jsonify(document_list)
            else:
                return "invalid token", 403
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/upload')
@api.doc(security='Bearer Auth')
class UploadFileController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])
        super(UploadFileController, self).__init__(*args, **kwargs)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    @api.doc(security='Bearer Auth')
    @token_authenticate
    def post(self):
        """UPLOAD FILE"""
        try:
            if request.method == 'POST':
                if 'file' not in request.files:
                    self.log.error(
                        'No file'
                    )
                    return "no file", 400
                file = request.files['file']
                if file.filename == '':
                    return 'No selected file', 400

                if file and self.allowed_file(file.filename):
                    # filename = secure_filename(file.filename)

                    extention = secure_filename(file.filename.split('.')[1])
                    filename = request.form.get(
                        'document_name', None).rstrip()+"."+extention
                    country = request.form.get(
                        'country', None).rstrip()
                    language = request.form.get(
                        'language', None).rstrip()
                    description = request.form.get(
                        'description', None).rstrip()
                    if(filename and language and description):
                        user = get_user_by_auth()
                        if(user):
                            self.file_service.upload_file_async(
                                filename, language, description, country, file, user)
                            return {'filename': filename, "status": "success"}, 200
                        else:
                            return 'Unauthorized', 401
                    else:
                        return 'Bad request', 400
                else:
                    return 'not supported file format', 400
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/showfile', methods=['GET', 'POST'])
class ShowFileController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])
        super(ShowFileController, self).__init__(*args, **kwargs)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    parser = None
    parser = api.parser()
    parser.add_argument('file_name', type=str, help='File name')

    # @api.doc(parser=parser, validate=True)
    def get(self):
        """DOWNLOAD PDF FILE"""
        try:
            args = self.req_parser.parse_args(strict=True)
            filename = args.get('file_name')
            if(filename):
                return send_from_directory(directory=current_app.config['ORIGINAL_FILE_FOLDER'], filename=filename)
            else:
                return 'Bad request', 400
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/download-document', methods=['GET', 'POST'])
class DownloadDocumentController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])
        super(DownloadDocumentController, self).__init__(*args, **kwargs)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    parser = None
    parser = api.parser()
    parser.add_argument('file_name', type=str, help='File name')

    def get(self):
        """DOWNLOAD PDF FILE"""
        try:
            args = self.req_parser.parse_args(strict=True)
            filename = args.get('file_name')
            if(filename):
                # //send_file // as_attachment = True
                return send_from_directory(directory=current_app.config['ORIGINAL_FILE_FOLDER'], filename=filename)
            else:
                return 'Bad request', 400
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/text-document-search', methods=['GET'])
class ShowDocumentSearch(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = PdfService()
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        parser.add_argument("text", type=str,
                            help='Paragraph text', required=True)
        self.req_parser = parser
        super(ShowDocumentSearch, self).__init__(*args, **kwargs)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    parser_ = None
    parser_ = api.parser()
    parser_.add_argument('file_name', type=str, help='File name')
    parser_.add_argument('text', type=str, help='Paragraph text')

    @api.doc(parser=parser_, validate=True)
    def get(self):
        """SEARCH TEXT IN DOCUMENT"""
        try:

            args = self.req_parser.parse_args(strict=True)
            file_name = args.get('file_name')
            text = args.get('text')
            return self.file_service.text_search_and_highligh(file_name, text)
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/download-document-test', methods=['GET'])
class TestDocumentController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = PdfService()
        super(TestDocumentController, self).__init__(*args, **kwargs)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    parser = None
    parser = api.parser()
    parser.add_argument('file_name', type=str, help='File name')

    def get(self):
        """DOWNLOAD PDF FILE"""
        try:
            self.file_service.test_highlight()
            return "ok"
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500
