
from flask_restful import Resource, reqparse, reqparse
import os

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
import json
from SPARQLWrapper import SPARQLWrapper, JSON


class WikibaseApi():
    def __init__(self):
        family = 'my'
        mylang = 'my'
        familyfile = current_app.config.get('PYWIKI_FAMILY_FILE')
        if not os.path.isfile(familyfile):
            print("family file %s is missing" % (familyfile))
        config2.register_family_file(family, familyfile)
        config2.password_file = current_app.config.get(
            'PYWIKI_USER_PASSWORD_FILE')
        config2.usernames['my']['my'] = current_app.config.get(
            'WIKI_USER_NAME')
        self.sparql = SPARQLWrapper(
            current_app.config.get('WIKI_SPARQL_END_POINT'))
        self.wikibase = pywikibot.Site("my", "my")
        self.wikibase_repo = self.wikibase.data_repository()

    def search_item(self, label):
        if label is None:
            return False
        params = {'action': 'wbsearchentities', 'format': 'json',
                  'language': 'en', 'type': 'item',
                  'limit': 100,
                  'search': label}
        request = self.wikibase._simple_request(**params)
        result = request.submit()
        return result
