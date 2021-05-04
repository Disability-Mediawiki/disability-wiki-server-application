

from flask_restful import Resource, reqparse, reqparse
import os
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app

from application.main.service.AuthenticationService import token_authenticate

api = Namespace('FILE_CONTROLLER', description='test controller initi')


@api.route('/')
@api.doc(security='Bearer Auth')
class FileController(Resource):
    # method_decorators = ['token_required']

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])

    # method_decorators

    # @api.doc(security='Bearer Auth')
    @token_authenticate
    def get(self):
        """GET ALL FILE"""
        # current_app.config["MAIN_PATH"]
        # self.searchWikiItem('CRPD Article 1')

        return "Hello from file"

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

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
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join('./resources/uploads', filename))
                # return {'data':filename}
                return jsonify({"data": "success"})
            else:
                return jsonify({"data": "not supported file format"})
