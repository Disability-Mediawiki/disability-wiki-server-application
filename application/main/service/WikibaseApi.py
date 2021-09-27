
from application.main.model.Enum.DocumentType import DocumentType
from application.main.service.SparqlService import SparqlService
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
        self.pywikibot = pywikibot
        self.wikibase_repo = self.wikibase.data_repository()
        self.sparql_service = SparqlService()

    def capitalize_first_letter(self, word):
        return word.capitalize()

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

    def search_exact_wiki_item(self, label):
        if label is None:
            return True
        params = {'action': 'wbsearchentities', 'format': 'json',
                  'language': 'en', 'type': 'item',
                  # 'limit': 1,
                  'search': label}
        request = self.wikibase._simple_request(**params)
        result = request.submit()
        print(result)
        if(len(result['search']) > 0):
            for item in result['search']:
                if (item.get('label') == label):
                    return True
        return False

    def create_document_entity(self, label, description, key, document_link, type):
        "CREATE DOCUMENT ENTITY"
        search_result = self.sparql_service.search_wiki_item_sparql(
            self.capitalize_first_letter(key.rstrip()))
        is_exist = self.search_exact_wiki_item(
            self.capitalize_first_letter(key.rstrip()))
        if (not search_result and not is_exist):
            data = {}
            print(f"inserting concept {key.rstrip()} ")
            data['labels'] = label
            data['descriptions'] = description
            new_item = self.pywikibot.ItemPage(self.wikibase_repo)
            new_item.editEntity(data)

            # insert statements
            new_claims = []
            claim_data = {}
            instance_claim = {}
            if(type == DocumentType.Document):
                # INSTANCE_OF_ DOCUMENT
                document_class_entity = self.pywikibot.ItemPage(
                    self.wikibase_repo, current_app.config['DOCUMENT_CLASS_QID'])
                document_class_entity.get()
                instance_of_property = self.pywikibot.PropertyPage(
                    self.wikibase_repo, current_app.config['INSTACE_OF_PROPERTY_PID'])
                instance_of_property.get()
                instance_claim = self.pywikibot.Claim(
                    self.wikibase_repo, instance_of_property.id, datatype=instance_of_property.type)
                instance_claim.setTarget(document_class_entity)
            else:
                # INSTANCE_OF_ WEB_CONTENT
                document_class_entity = self.pywikibot.ItemPage(
                    self.wikibase_repo, current_app.config['WEB_CONTENT_CLASS_QID'])
                document_class_entity.get()
                instance_of_property = self.pywikibot.PropertyPage(
                    self.wikibase_repo, current_app.config['INSTACE_OF_PROPERTY_PID'])
                instance_of_property.get()
                instance_claim = self.pywikibot.Claim(
                    self.wikibase_repo, instance_of_property.id, datatype=instance_of_property.type)
                instance_claim.setTarget(document_class_entity)

            # DOCUMENT_URI
            document_uri_property = self.pywikibot.PropertyPage(
                self.wikibase_repo, current_app.config['DOCUMENT_REFERENCE_URI_PROPERTY_PID'])
            document_uri_property.get()
            document_uri_claim = self.pywikibot.Claim(
                self.wikibase_repo, document_uri_property.id, datatype=document_uri_property.type)
            document_uri_claim.setTarget(document_link)

            # Save all claim
            new_claims.append(instance_claim.toJSON())
            new_claims.append(document_uri_claim.toJSON())
            claim_data['claims'] = new_claims
            new_item.editEntity(claim_data)

            return new_item
        else:
            entity = self.sparql_service.get_item_with_sparql(
                self.capitalize_first_letter(key.rstrip()))
            return entity

    def create_paragraph_entity(self, label, description, text, document_entity, sub_topics, lang):
        "CREATE PARAGRAPH ENTITY"

        data = {}
        print(f"inserting paragarph")
        data['labels'] = label
        data['descriptions'] = description
        paragraph_item = pywikibot.ItemPage(self.wikibase_repo)
        paragraph_item.editEntity(data)

        # insert statements

        # INSTANCE_OF
        paragraph_class_entity = self.pywikibot.ItemPage(
            self.wikibase_repo, current_app.config['PARAGRAPH_CLASS_QID'])
        paragraph_class_entity.get()
        instance_of_property = self.pywikibot.PropertyPage(
            self.wikibase_repo, current_app.config['INSTACE_OF_PROPERTY_PID'])
        instance_of_property.get()
        instance_claim = self.pywikibot.Claim(
            self.wikibase_repo, instance_of_property.id, datatype=instance_of_property.type)
        instance_claim.setTarget(paragraph_class_entity)
        paragraph_item.addClaim(
            instance_claim, summary=u'Adding claim to paragraph')

        # PART_OF
        part_of_property = self.pywikibot.PropertyPage(
            self.wikibase_repo,  current_app.config['PART_OF_DOCUMENT_PROPERTY_PID'])
        part_of_property.get()
        part_of_claim = self.pywikibot.Claim(
            self.wikibase_repo, part_of_property.id, datatype=part_of_property.type)
        part_of_claim.setTarget(document_entity)
        paragraph_item.addClaim(
            part_of_claim, summary=u'Adding claim to paragraph')

        # HAS_TEXT
        has_text_property = self.pywikibot.PropertyPage(
            self.wikibase_repo,  current_app.config['HAS_TEXT_PROPERTY_PID'])
        has_text_property.get()
        has_text_claim = self.pywikibot.Claim(
            self.wikibase_repo, has_text_property.id, datatype=has_text_property.type)
        has_text_claim.setTarget(text)
        paragraph_item.addClaim(
            has_text_claim, summary=u'Adding claim to paragraph')

        if(paragraph_item):

            # SUP_TOPICS
            for sub_topic in sub_topics:
                ""
                topic_entity = self.create_sub_topic(sub_topic.label, paragraph_item,
                                                     document_entity, lang)
                topic_entity.get()
                if(topic_entity):
                    # HAS_TOPIC
                    has_topic_property = self.pywikibot.PropertyPage(
                        self.wikibase_repo, current_app.config['HAS_TOPIC_PROPERTY_PID'])
                    has_topic_property.get()
                    has_topic_claim = self.pywikibot.Claim(
                        self.wikibase_repo, has_topic_property.id, datatype=has_topic_property.type)
                    has_topic_claim.setTarget(topic_entity)
                    paragraph_item.addClaim(
                        has_topic_claim, summary=u'add claim to paragraph')

            # HAS_PARAGRAPH
            has_paragraph_property = self.pywikibot.PropertyPage(
                self.wikibase_repo, current_app.config['HAS_PARAGRAPH_PROPERTY_PID'])
            has_paragraph_property.get()
            has_paragraph_claim = self.pywikibot.Claim(
                self.wikibase_repo, has_paragraph_property.id, datatype=has_paragraph_property.type)
            has_paragraph_claim.setTarget(paragraph_item)
            document_entity.addClaim(
                has_paragraph_claim, summary=u'Adding claim to document')

            return paragraph_item

        else:
            return False

    def create_sub_topic(self, topic, paragraph_entity, document_entity, lang):
        "CREATE SUB TOPIC ENTITY"
        topic_entity = {}
        search_result = self.sparql_service.search_wiki_item_sparql(
            self.capitalize_first_letter(topic.rstrip()))
        is_exist = self.search_exact_wiki_item(
            self.capitalize_first_letter(topic.rstrip()))
        if (not search_result and not is_exist):
            # CHECK IS ALIAS EXIST
            is_alias_exist = self.sparql_service.search_wiki_item_by_alias(
                self.capitalize_first_letter(topic.rstrip()))
            if (not is_alias_exist):
                # IF NOT TOPIC ALREADY EXIST, CREATE NEW TOPIC
                data = {}
                label = {lang: topic.capitalize().rstrip()}
                description = {
                    lang: topic.capitalize().rstrip()+" entity"}
                data['labels'] = label
                data['descriptions'] = description
                topic_entity = self.pywikibot.ItemPage(self.wikibase_repo)
                topic_entity.editEntity(data)
                # return topic_entity
            else:
                # GET TOPIC BY ALIAS
                topic_entity = self.sparql_service.get_item_with_sparql_by_alias(
                    self.capitalize_first_letter(topic.rstrip()))
                topic_entity.get()

        else:
            topic_entity = self.sparql_service.get_item_with_sparql(
                self.capitalize_first_letter(topic.rstrip()))
            topic_entity.get()
        if(topic_entity):
            # MENTIONED_IN
            metnioned_in_property = self.pywikibot.PropertyPage(
                self.wikibase_repo, current_app.config['MENTIONED_IN_PROPERTY_PID'])
            metnioned_in_property.get()
            metnioned_in_claim = self.pywikibot.Claim(
                self.wikibase_repo, metnioned_in_property.id, datatype=metnioned_in_property.type)
            paragraph_entity.get()
            metnioned_in_claim.setTarget(paragraph_entity)
            topic_entity.addClaim(metnioned_in_claim,
                                  summary=u'Adding claim to topics')
            return topic_entity
        else:
            return False
