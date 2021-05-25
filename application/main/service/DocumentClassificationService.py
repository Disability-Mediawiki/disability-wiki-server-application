
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
import json
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from .. import db
from application.main.model.ClassificationResult import ClassificationResult
from application.main.model.Paragraph import Paragraph
from application.main.model.ParagraphTag import ParagraphTag
from application.main.model.Document import Document
from application.main.model.User import User
from application.main.model.Enum.ClassificationResultStatus import ClassificationResultStatus


class DocumentClassificationService():
    def __init__(self):
        ""

    def get_all_paragraphs_and_tags(self, document_name):
        paragraph_list = db.session.query(Paragraph).\
            join(Document, Document.id == Paragraph.document_id).\
            all()
        b = dict(paragraph_list)
        result = json.dumps(
            [[ob.__dict__ for ob in lst.paragraph_tags] for lst in b])
        return result

    def save_classification_result(self, document, paragraphs):

        classification = ClassificationResult(
            document_id=document.id,
            status=ClassificationResultStatus.Updated,
        )
        db.session.add(classification)
        db.session.flush()
        count = 1
        for paragraph in paragraphs:
            pr = Paragraph(
                label=document.document_name+" paragraph " + str(count),
                paragraph=paragraph.get('paragraph'),
                classification_result_id=classification.id,
                document_id=document.id
            )
            db.session.add(pr)
            db.session.flush()
            for tag in paragraph.get('tags'):
                p_tag = ParagraphTag(
                    label=tag.get('text'),
                    paragraph_id=pr.id
                )
                db.session.add(p_tag)
            count += 1

        db.session.commit()
        return True
