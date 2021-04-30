
from flask_restful import Resource,reqparse,reqparse
import os
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import  FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request,jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace

api = Namespace('FILE_CONTROLLER', description='test controller initi')

# api = Api()


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
# @api.route('/file', endpoint='my-resource')
class FileController(Resource):
    def __init__(self,*args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ALLOWED_EXTENSIONS = set(['txt', 'pdf','png',  'jpg', 'jpeg', 'gif'])
        # Create a request parser
        # parser = reqparse.RequestParser()
        # parser.add_argument("image", type=datastructures.FileStorage, location='files')
        # self.req_parser = parser

    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("pdf", type=FileStorage, location='files')
    #     self.req_parser = parser
    #     # The image is retrieved as a file
    #     image_file = self.req_parser.parse_args(strict=True).get("pdf", None)
    #
    #
    #     if image_file:
    #         # Get the byte content using `.read()`
    #         image = image_file.read()
    #         filename = secure_filename(image_file.filename)
    #         image_file.save(os.path.join('./resources/uploads', filename))
    #         # Now do something with the image...
    #         return "Yay, you sent an image!"
    #     else:
    #         return "No image sent :("
    #
    def get(self,public_id):
        """GET ALL FILE"""
        return "Hello from file"+public_id





    # def post(self, fname):
    #     file = request.files['file']
    #     if file and allowed_file(file.filename):
    #         # From flask uploading tutorial
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('uploaded_file', filename=filename))
    #     else:
    #         # return error
    #         return {'False'}

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
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

