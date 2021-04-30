import os

# Pywikibot
import pywikibot
from pywikibot import config2
# from pywikibot.data import api
# import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON
# /Pywikibot


def config_pywikibot():
    family = 'my'
    mylang = 'my'
    familyfile = os.path.relpath("./config/my_family.py")
    if not os.path.isfile(familyfile):
        print("family file %s is missing" % (familyfile))
    config2.register_family_file(family, familyfile)
    config2.password_file = "user-password.py"
    config2.usernames['my']['my'] = 'WikibaseAdmin'

    wikibase = pywikibot.Site("my", "my")
    wikibase_repo = wikibase.data_repository()
    print('connected')

    data = {}
    data['labels'] = {'en': 'TestITEM FROM FLASK',
                      'fr': 'item test france'}
    data['descriptions'] = {'en': 'TestITEM FROM FLASK'}
    new_item = pywikibot.ItemPage(wikibase_repo)
    new_item.editEntity(data)
    print(new_item.id)


config_pywikibot()
# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
