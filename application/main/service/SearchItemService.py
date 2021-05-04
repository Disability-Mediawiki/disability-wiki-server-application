

from flask_restful import Resource, reqparse, reqparse
import os

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app

from application.main.service.WikibaseApi import WikibaseApi
from application.main.service.SparqlService import SparqlService


class SearchItemService():
    def __init__(self):
        self.wikibase_api = WikibaseApi()
        self.sparql_service = SparqlService()

    def public_search(self, label):
        wikiApi = WikibaseApi()
        results = wikiApi.search_item(label)
        search_result = []
        for result in results['search']:
            item = {}
            properties = self.sparql_service.get_all_properties_of_item(
                result.get('id'))
            item[result.get('id')] = {
                'label': result['label'],
                'description': result['description'],
                'concepturi': result['concepturi'],
                'properties': properties['results']['bindings']
            }
            search_result.append({
                'label': result['label'],
                'description': result['description'],
                'concepturi': result['concepturi'],
                'properties': properties['results']['bindings']
            })
        return search_result

    def get_all_properties_of_item(self, qid):
        ""
