

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
# Pywikibot
import pywikibot
from pywikibot import config2
# from pywikibot.data import api
# import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON
app = Flask(__name__)

# /Pywikibot

api = Namespace('FILE_CONTROLLER', description='test controller initi')


@api.route('/')
class FileController(Resource):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png',  'jpg', 'jpeg', 'gif'])

    def get(self):
        """GET ALL FILE"""
        current_app.config["MAIN_PATH"]
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

    # Searches a concept based on its label with a API call

    def searchWikiItem(self, label):

        family = 'my'
        mylang = 'my'
        # familyfile = os.path.relpath("./config/my_family.py")
        # familyfile = os.path.join(
        #     app.instance_path, 'config', 'my_family.py')
        # familyfile = os.path.join(
        #     app.root_path, 'config', 'my_family.py')
        familyfile = os.path.join(
            app.root_path.rsplit('\\', 1)[0].rsplit('\\', 1)[0], 'config', 'my_family.py')
        if not os.path.isfile(familyfile):
            print("family file %s is missing" % (familyfile))
        config2.register_family_file(family, familyfile)
        # config2.password_file = "user-password.py"
        config2.password_file = app.root_path.rsplit(
            '\\', 1)[0].rsplit('\\', 1)[0]+'\\user-password.py'
        config2.usernames['my']['my'] = 'WikibaseAdmin'

        wikibase = pywikibot.Site("my", "my")
        wikibase_repo = wikibase.data_repository()
        print('connected')

        data = {}
        data['labels'] = {'en': 'TestITEM FROM FLASK',
                          'fr': 'item test france'}
        data['descriptions'] = {'en': 'TestITEM FROM FLASK234'}
        new_item = pywikibot.ItemPage(wikibase_repo)
        new_item.editEntity(data)
        print(new_item.id)
        # sparql = SPARQLWrapper(
        #     'http://localhost:8989/bigdata/namespace/wdq/sparql')

        # if label is None:
        #     return True
        # params = {'action': 'wbsearchentities', 'format': 'json',
        #           'language': 'en', 'type': 'item',
        #           # 'limit': 1,
        #           'search': label}
        # request = wikibase._simple_request(**params)
        # result = request.submit()
        # print(result)
        # if(len(result['search']) > 0):
        #     for item in result['search']:
        #         if (item.get('label') == label):
        #             return True
        # return False
