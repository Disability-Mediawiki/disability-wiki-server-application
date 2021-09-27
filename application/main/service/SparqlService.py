

from flask_restful import Resource, reqparse, reqparse
import os
from functools import reduce
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

    def get_dic_value_safe(self, dictionary, keys, default=None):
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

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
        if (results.get('results', None) is not None and
                results.get('results').get('bindings') is not None and
                type(results.get('results').get('bindings')) is list and
                len(results.get('results').get('bindings')) > 0 and
                results.get('results').get('bindings')[0] is not None and
                results.get('results').get('bindings')[0].get('s', None) is not None and
                results.get('results').get('bindings')[0].get(
                's').get('value', None) is not None
                ):
            item_qid = results['results']['bindings'][0]['s']['value'].split(
                "/")[-1]
            if(item_qid):
                item = self.pywikibot.ItemPage(self.wikibase_repo, item_qid)
                return item
            else:
                return False
        else:
            return False

    # get items with sparql by alias name

    def get_item_with_sparql_by_alias(self, label):
        query = """
             SELECT DISTINCT ?label ?s where
                    {
                      ?s ?p ?o;
                       skos:altLabel ?label .
                      FILTER(lang(?label)='fr' || lang(?label)='en')
                      FILTER(?label = '""" + label + """'@en)
                    }
             """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        if (results.get('results', None) is not None and
                results.get('results').get('bindings') is not None and
                type(results.get('results').get('bindings')) is list and
                len(results.get('results').get('bindings')) > 0 and
                results.get('results').get('bindings')[0] is not None and
                results.get('results').get('bindings')[0].get('s', None) is not None and
                results.get('results').get('bindings')[0].get(
                's').get('value', None) is not None
                ):
            item_qid = results['results']['bindings'][0]['s']['value'].split(
                "/")[-1]
            if(item_qid):
                item = self.pywikibot.ItemPage(self.wikibase_repo, item_qid)
                return item
            else:
                return False
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

    def search_wiki_item_by_alias(self, label):
        query = """
              SELECT DISTINCT ?s ?label  where
                {
                ?s ?p ?o;
                    skos:altLabel ?label .
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
