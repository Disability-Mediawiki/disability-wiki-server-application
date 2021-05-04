

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


"""
SELECT ?wdLabel ?ps_Label ?wdpqLabel ?pq_Label {
  VALUES (?company) {(wd:Q95)}
  
  ?company ?p ?statement .
  ?statement ?ps ?ps_ .
  
  ?wd wikibase:claim ?p.
  ?wd wikibase:statementProperty ?ps.
  
  OPTIONAL {
  ?statement ?pq ?pq_ .
  ?wdpq wikibase:qualifier ?pq .
  }
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} ORDER BY ?wd ?statement ?ps_

//

SELECT ?a ?aLabel ?propLabel ?b ?bLabel
WHERE
{
  ?item rdfs:label "Google"@en.
  ?item ?a ?b.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
  ?prop wikibase:directClaim ?a .
}

//
SELECT ?a ?aLabel ?propLabel ?b ?bLabel
WHERE
{
#   ?item rdfs:label "Google"@en.
  wd:Q95 ?a ?b.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
  ?prop wikibase:directClaim ?a .
}

"""
