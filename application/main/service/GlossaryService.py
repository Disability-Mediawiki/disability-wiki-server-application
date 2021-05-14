
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from .. import db, flask_bcrypt
from application.main.service.SynonymService import SynonymService
from application.main.model.GlossaryTag import GlossaryTag


class GlossaryService():
    def __init__(self):
        self.synonym_service = SynonymService()

    def get_all(self):
        glossary_list = GlossaryTag.query.all()
        return glossary_list

    def create(self, glossaries):
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

    def create_glossary(self, glossary_tag, synonyms=None):
        glossary_tag = GlossaryTag(
            label=glossary_tag
        )
        db.session.add(glossary_tag)
        db.session.commit()
        if(synonyms):
            for synonym in synonyms:
                self.synonym_service.create_synonym(synonym, glossary_tag.id)
        return glossary_tag
