

from flask_restful import Resource, reqparse, reqparse
import os
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
import json
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from flask_cors import cross_origin
from application.main.service.AuthenticationService import token_authenticate, token_authenticate_admin
import csv
import pandas as pd
api = Namespace('FILE_CONTROLLER', description='test controller initi')


# @api.route('/download/<file_name>')
@api.route('/download')
@api.doc(security='Bearer Auth')
class DownloadExtractionController(Resource):
    parser_ = None

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])
        parser = reqparse.RequestParser()
        parser.add_argument("file_name", type=str,
                            help='File name', required=True)
        self.req_parser = parser
        parser_ = parser

    # @token_authenticate
    @api.expect(parser_, validate=True)
    def get(self):
        args = self.req_parser.parse_args(strict=True)
        """GET ALL FILE"""
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

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    # @api.doc(security='Bearer Auth')
    def post(self):
        """UPLOAD FILE"""
        print('came here')
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
