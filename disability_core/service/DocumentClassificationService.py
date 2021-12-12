
# /*
# CLASSIFY DOCUMENT SERVICE
#
# */

import logging
import json
import re
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from application import db
from application.main.model.Paragraph import Paragraph
from application.main.model.ParagraphTag import ParagraphTag
from application.main.model.Document import Document
from application.main.model.User import User
from application.main.service.FastTextService import FastTextService


class DocumentClassificationService():
    def __init__(self):
        self.fast_text_service = FastTextService()

    def classify_paragraph(self, paragraph):
        try:
            paragraph_tags = self.fast_text_service.classify_paragraph(
                re.sub('\?|\#|\!|\/|\;|\:|\$','',paragraph.paragraph.rstrip().lstrip()))
            if(paragraph_tags):
                for tag in paragraph_tags[0][0]:
                    new_tag = ParagraphTag(
                        label=tag.split('__label__')[1],
                        paragraph_id=paragraph.id
                    )
                    db.session.add(new_tag)
                db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise
