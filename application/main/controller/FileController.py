

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
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('FILE_CONTROLLER', description='File operations')


# @api.route('/download/<file_name>')
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
        # return json.dumps(extraction_results), 200

    # def get(self, file_name):
    #     """GET ALL FILE"""
    #     extraction_results = []
    #     data = pd.ExcelFile(os.path.join(
    #         current_app.config['RESULT_FOLDER'], file_name))
    #     return json.dumps(data), 200
    #     # return json.dumps(extraction_results), 200


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
        user = get_user_by_auth()
        if(user):
            document_list = self.file_service.get_all_document(user)
            if(document_list):
                # json_res = json.dumps([ob.__dict__ for ob in document_list])
                # return json.dumps(document_list, default=str)
                return jsonify(document_list)
            else:
                return "No documents found", 404
        else:
            return "invalid token", 403


@api.route('/get-pending-document', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetPendingDocumentListController(Resource):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        super(GetPendingDocumentListController, self).__init__(*args, **kwargs)

    def get(self):
        """GET ALL PENDING DOCUMENTS"""
        user = get_user_by_auth()
        if(user):
            document_list = self.file_service.get_all_pending_document(user)
            if(document_list):
                # return json.dumps(document_list, default=self.obj_dict)
                return jsonify(document_list)
            else:
                return "No documents found", 404
        else:
            return "invalid token", 403


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
        if request.method == 'POST':

            if 'file' not in request.files:
                self.log.error(
                    'No file'
                )
                return "no file"
            file = request.files['file']
            if file.filename == '':
                return 'No selected file'

            if file and self.allowed_file(file.filename):
                # filename = secure_filename(file.filename)

                extention = secure_filename(file.filename.split('.')[1])
                filename = request.form.get(
                    'document_name', None).rstrip()+extention
                country = request.form.get(
                    'country', None).rstrip()

                user = get_user_by_auth()
                self.file_service.upload_file(filename, country, file, user)
                return {'filename': filename, "status": "success"}, 200
            else:
                return {"data": "not supported file format"}


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
        # args = self.req_parser.parse_args(strict=True)
        filename = 'CRDP.pdf'
        # current_app.config['UPLOAD_FOLDER']
        # uploads = 'F:\\Internship York\\Repo\\Disability-Media-Wiki\\flask\\server-flask-restplus\\resources\\uploads'
        return send_from_directory(directory=current_app.config['ORIGINAL_FILE_FOLDER'], filename=filename)

        # return send_file(open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb'), attachment_filename='pdffile.pdf')

        # with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb')as f:
        #     response = make_response(f)
        #     response.headers.set('Content-Disposition',
        #                          'attachment', filename='test.pdf')
        #     response.headers.set('Content-Type', 'application/pdf')
        #     return response

        # with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)) as f:
        # file_content = f.read()
        # response = make_response(file_content, 200)
        # response.headers['Content-type'] = 'application/pdf'
        # response.headers['Content-disposition'] = ...

        # return send_file(
        #     f,
        #     as_attachment=True,
        #     attachment_filename='annotated.pdf',
        #     mimetype='application/pdf')

        # return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'],
        #                            filename=filename,
        #                            mimetype='application/pdf')

        # try:
        #     return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), attachment_filename='ohhey.pdf')
        # except Exception as e:
        #     return str(e)
        # if args.file_name and self.allowed_file(args.file_name):

        # with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb') as static_file:
        #     return send_file(static_file, attachment_filename='file.pdf')

        # else:
        #     return "File format not supported", 415


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
        args = self.req_parser.parse_args(strict=True)
        filename = args.get('file_name')
        # //send_file // as_attachment = True
        return send_from_directory(directory=current_app.config['ORIGINAL_FILE_FOLDER'], filename=filename, as_attachment=False)


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
        self.file_service.test_highlight()
        return "ok"
