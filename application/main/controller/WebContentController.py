
# /*
# WEB CONTENT CONTROLLER
# UPLOAD WEB CONTENTS SUCH AS BLOG POSTS, WEB SITES ETC
# */
import logging
import os
import requests
from bs4 import BeautifulSoup
from application.main.service.AuthenticationService import (
    token_authenticate, token_authenticate_admin, get_user_by_auth)
from application.main.service.AuthService import AuthService
from application.main.service.WebContentService import WebContentService
from flask import Flask, current_app, jsonify, make_response, request
# from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource, reqparse


api = Namespace('WEB CONTENT CONTROLLER',
                description='Manage web contents [Blogs, Website etc]')


@api.route('/')
class WebContentController(Resource):

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        parser = reqparse.RequestParser()
        self.web_content_service = WebContentService()
        parser.add_argument("link", type=str, help='website link')
        self.req_parser = parser
        super(WebContentController, self).__init__(*args, **kwargs)

    parser = None
    parser = api.parser()
    parser.add_argument('link', type=str, help='website link')

    @api.doc(parser=parser, validate=True)
    @token_authenticate
    def get(self):
        """GET CONTENTS FROM WEB RESOURCE"""
        args = self.req_parser.parse_args(strict=True)
        link = args.link
        try:
            paragraphs = self.web_content_service.browse_and_scrape(link)

            return paragraphs, 200
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


@api.route('/upload')
class UploadWebContentController(Resource):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.web_content_service = WebContentService()
        parser = reqparse.RequestParser()
        parser.add_argument("document", type=dict,
                            help='Document object is missing', required=True)
        parser.add_argument("paragraphs",
                            type=dict, action='append',  help='paragraphs',  required=True)
        self.req_parser = parser
        self.req_parser = parser
        super(UploadWebContentController, self).__init__(*args, **kwargs)

    @token_authenticate
    def post(self):
        """UPLOAD WEB CONTENTS"""
        args = self.req_parser.parse_args(strict=True)
        try:
            user = get_user_by_auth()
            paragraphs = args.get('paragraphs')
            doc = args.get('document')
            if user:
                self.web_content_service.upload_web_content(doc.get('document_name'), doc.get('language'), doc.get(
                    'description'), doc.get('country'), paragraphs, doc.get('link'), user)
                return "success", 201
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500
