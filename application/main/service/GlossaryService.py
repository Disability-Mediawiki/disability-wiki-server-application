
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
import json
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from .. import db, flask_bcrypt
from application.main.service.SynonymService import SynonymService
from application.main.model.GlossaryTag import GlossaryTag
from application.main.model.Synonym import Synonym


class GlossaryService():
    def __init__(self):
        self.synonym_service = SynonymService()

    def get_all(self):
        # glossary_list = GlossaryTag.query.all()
        glossary_list = db.session.query(GlossaryTag).\
            join(Synonym, Synonym.glossary_tag_id == GlossaryTag.id).all()
        glossary_tag_list = []
        for glossary_tag in glossary_list:
            synonyms = glossary_tag.synonyms
            synonyms_dict = []
            for synonym in synonyms:
                synonyms_dict.append(
                    {'id': synonym.id, 'label': synonym.label, 'glossary_tag_id': synonym.glossary_tag_id})
            glossary_tag_list.append(
                {'label': glossary_tag.label, 'id': glossary_tag.id, 'synonyms': synonyms_dict})
        return glossary_tag_list

    def get_all_as_flat_list(self):
        glossary_list = GlossaryTag.query.all()
        synonym_list = self.synonym_service.get_all()
        glossary_tag_list = []
        for glossary_tag in glossary_list:
            glossary_tag_list.append(
                {'label': glossary_tag.label.capitalize(), 'id': glossary_tag.id})

        for synonym in synonym_list:
            glossary_tag_list.append(
                {'id': synonym.id, 'label': synonym.label.capitalize(), 'glossary_tag_id': synonym.glossary_tag_id})
        glossary_tag_list.sort(key=lambda x: x.get('label'))
        return glossary_tag_list

    def create(self, glossaries):
        try:
            for glossary in glossaries:
                glossary_tag = GlossaryTag(
                    label=glossary.get('label')
                )
                db.session.add(glossary_tag)
                db.session.commit()
                if(glossary.get('synonyms', None) and len(glossary.get('synonyms')) > 0):
                    for synonym in glossary.get('synonyms'):
                        self.synonym_service.create_synonym(
                            synonym.get('label'), glossary_tag.id)
            return glossary_tag
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def create_glossary(self, glossary_tag, synonyms=None):
        try:
            glossary_tag = GlossaryTag(
                label=glossary_tag
            )
            db.session.add(glossary_tag)
            db.session.commit()
            if(synonyms):
                for synonym in synonyms:
                    self.synonym_service.create_synonym(
                        synonym, glossary_tag.id)
            return glossary_tag
        except Exception as e:
            print(e)
            db.session.rollback()
            raise
