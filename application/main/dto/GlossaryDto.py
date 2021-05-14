
from flask_restplus import Resource, Api, Namespace, fields
from ..model import Synonym


class GlossaryDto:
    api = Namespace('GLOSSARY_CONTROLLER', description='Glossary operations')
    glossary_field = api.model('glossary', {
        'label': fields.String(required=True, description='Glossary label'),
        'synonyms': fields.List(fields.String, description='Synonym list'),
    })
    glossary = api.model('Glossary', {
        'glossary': fields.List(fields.Nested(glossary_field))
        # fields.Nested(glossary_field, required=True)
    })

    # glossary = api.model('glossary', {
    #     'label': fields.String(required=True, description='Glossary label'),
    #     'synonyms': fields.List(fields.String, description='Synonym list'),
    # })
