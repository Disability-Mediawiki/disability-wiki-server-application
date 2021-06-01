

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


class SparqlService():
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
        self.pywikibot = pywikibot
        self.wikibase_repo = self.wikibase.data_repository()

    def get_all_properties_of_item(self, qid):
        query = """
              SELECT ?a ?aLabel ?propLabel ?b ?bLabel
              WHERE
              {
                wd:"""+qid+""" ?a ?b.
                SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
                ?prop wikibase:directClaim ?a .
              }
             """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        print(results)
        return results

    # get items with sparql
    def get_item_with_sparql(self, label):
        query = """
             select ?label ?s where
                    {
                      ?s ?p ?o.
                      ?s rdfs:label ?label .
                      FILTER(lang(?label)='fr' || lang(?label)='en')
                      FILTER(?label = '""" + label + """'@en)
    
                    }
             """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        item_qid = results['results']['bindings'][0]['s']['value'].split(
            "/")[-1]
        if(item_qid):
            item = self.pywikibot.ItemPage(self.wikibase_repo, item_qid)
            return item
        else:
            return False
    # Searches a concept based on its label on Tripple store

    def search_wiki_item_sparql(self, label):
        query = """
             select ?label ?s where
                    {
                      ?s ?p ?o.
                      ?s rdfs:label ?label .
                      FILTER(lang(?label)='fr' || lang(?label)='en')
                      FILTER(?label = '""" + label + """'@en)
    
                    }
             """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        if (len(results['results']['bindings']) > 0):
            return True
        else:
            return False
