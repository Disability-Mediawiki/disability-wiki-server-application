

import csv
import json
import logging
import os

import pandas as pd
from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin)
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

api = Namespace('FILE_CONTROLLER', description='test controller initi')


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
                        {'tag': tags, 'paragraph': row[0]})
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


@api.route('/upload')
@api.doc(security='Bearer Auth')
class UploadFileController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])
        super(UploadFileController, self).__init__(*args, **kwargs)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    # @api.doc(security='Bearer Auth')

    def post(self):
        """UPLOAD FILE"""
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                self.log.error(
                    'No file'
                )
                return "no file"
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                return 'No selected file'
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename))
                # file.save(os.path.join('./resources/uploads', filename))
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
