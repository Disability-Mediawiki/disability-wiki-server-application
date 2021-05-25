
import os
# from werkzeug import FileStorage,datastructures
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask_restplus import Resource, Api, Namespace, reqparse
from flask import current_app
# from main.service.WikibaseApi import WikibaseApi
from application.main.service.SearchItemService import SearchItemService

api = Namespace('WIKIBASE_CONTROLLER', description='Wikibase Api Operations')


@api.route('/search')
@api.doc(security='apikey')
@api.param('keyword', 'Search keyword')
class WikibaseController(Resource):
    parser = None

    def __init__(self, *args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "keyword", type=str, help='Search keyword', required=True)
        self.req_parser = parser
        self.log = logging.getLogger(__name__)
        self.search_service = SearchItemService()

    # @api.expect(parser)
    def get(self):
        """search tests"""
        args = self.req_parser.parse_args(strict=True)
        result = self.search_service.public_search(args.get('keyword'))
        return jsonify(result)
