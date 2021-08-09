# /*
# GLOSSARY MANAGEMENT CONTROLLER
# */
import json
import logging
import os
from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin)
from flask import (Flask, current_app, jsonify, make_response, request,
                   send_file, send_from_directory)
from flask_cors import cross_origin
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource, marshal_with, fields
from application.main.dto.GlossaryDto import GlossaryDto
from application.main.service.GlossaryService import GlossaryService

api = GlossaryDto.api
_glossary = GlossaryDto.glossary

# /*
# GET ALL GLOSSARY TERMS
# */


@api.route('/get-all', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetAllGlossaryController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.glossary_service = GlossaryService()
        super(GetAllGlossaryController, self).__init__(*args, **kwargs)

    def get(self):
        """GET ALL GLOSSARY TERMS"""
        glossary_list = self.glossary_service.get_all()
        return glossary_list, 200

# /*
# GET ALL GLOSSARY AND SYNONYMS IN ONE DIMENTION ARRAY
# */


@api.route('/get-all-flat', methods=['GET'])
@api.doc(security='Bearer Auth')
class GetAllFlatGlossaryController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.glossary_service = GlossaryService()
        super(GetAllFlatGlossaryController, self).__init__(*args, **kwargs)

    def get(self):
        """GET ALL GLOSSARY AND SYNONYMS-FLAT LIST"""
        glossary_list = self.glossary_service.get_all_as_flat_list()
        return glossary_list, 200

# /*
# CREATE GLOSSARY TERM
# */


@api.route('/create')
class CreateGlossaryController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.glossary_service = GlossaryService()
        parser = reqparse.RequestParser()
        parser.add_argument("glossary",
                            type=dict, help='Glossary is required', action='append', required=True)
        self.req_parser = parser
        super(CreateGlossaryController, self).__init__(*args, **kwargs)

    @api.expect(_glossary, validate=True)
    def post(self):
        """CREATE GLOSSARY"""
        args = self.req_parser.parse_args(strict=True)
        try:
            glossaries = args.get('glossary')
            self.glossary_service.create(glossaries)
            responseObject = {
                'status': 'Success'
            }
            return responseObject, 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500
