

import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from .. import db

from application.main.model.Synonym import Synonym


class SynonymService():
    def __init__(self):
        ""

    def get_all(self):
        glossary_list = Synonym.query.all()
        return glossary_list

    def create_synonym(self, synony_tag, glossary_tag_id):
        synonym = Synonym(
            label=synony_tag,
            glossary_tag_id=glossary_tag_id,
        )
        db.session.add(synonym)
        db.session.commit()
        return synonym
