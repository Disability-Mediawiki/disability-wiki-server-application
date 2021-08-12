# /*
# FILE CONTROLLER
# */

import csv
import json
import logging
import os

from application.main.service.AuthenticationService import (
    get_user_by_auth, token_authenticate, token_authenticate_admin)
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

# /*
# GET ALL DOCUMENTS BY USER
# */


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

# /*
# GET PENDING DOCUMENTS BY USER [CLASSIFIED, PROCESSING]
# */


@api.route('/get-pending-document', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetPendingDocumentListController(Resource):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        super(GetPendingDocumentListController, self).__init__(*args, **kwargs)

    def get(self):
        """GET ALL PENDING DOCUMENTS [CLASSIFIED, PROCESSING]"""
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

# /*
# UPLOAD NEW DOCUMENT
# */


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
        """UPLOAD DOCUMENT"""
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

# /*
# GET PDF DOCOMENT FILE  args:[file_name]
# */


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

# /*
# GET DOCUMNT WITH HIGHLIGHTED TEXT CONTENT - args [document, search_text]
# */


@api.route('/text-document-search', methods=['GET'])
class DocumentContentSearchController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = PdfService()
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        parser.add_argument("text", type=str,
                            help='Paragraph text', required=True)
        self.req_parser = parser
        super(DocumentContentSearchController, self).__init__(*args, **kwargs)

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


# /*
# CHECK ALREADY DOCUMENT NAME EXIST - args [text]
# */


@api.route('/is-name-exit', methods=['GET'])
class DocumentNameValidationController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        super(DocumentNameValidationController, self).__init__(*args, **kwargs)

    parser_ = None
    parser_ = api.parser()
    parser_.add_argument('file_name', type=str, help='File name')

    @api.doc(parser=parser_, validate=True)
    def get(self):
        """SEARCH IS DOCUMENT NAME EXIST"""
        try:

            args = self.req_parser.parse_args(strict=True)
            file_name = args.get('file_name')
            return self.file_service.is_name_exit(file_name), 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500
