
from application.main.model.TrainingData import TrainingData
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
from application.main.service.FastTextService import FastTextService
from application.main.model.Enum.ClassificationResultStatus import ClassificationResultStatus


class DocumentClassificationService():
    def __init__(self):
        self.fast_text_service = FastTextService()

    def get_all_paragraphs_and_tags_by_user(self, document_name, document_id, user):
        paragraph_list = db.session.query(Paragraph).\
            join(ClassificationResult, ClassificationResult.id == Paragraph.classification_result_id).\
            join(Document, Document.id == ClassificationResult.document_id).\
            join(User, User.id == Document.user_id).\
            where(Document.document_name == document_name).\
            where(User.id == user.id).\
            where(Document.id == document_id).\
            all()
        # list = {x.id: x for x in paragraph_list}
        list = []
        for paragraph in paragraph_list:
            tags = []
            for tag in paragraph.paragraph_tags:
                tags.append({'text': tag.label, 'id': tag.id})
            list.append(
                {'classification_id': paragraph.classification_result_id, 'id': paragraph.id, 'key': str(paragraph.id)+"_"+str(paragraph.classification_result_id), 'tag': tags,
                 'paragraph': paragraph.paragraph})

        return list

    def get_all_paragraphs_and_tags(self, document_name):
        paragraph_list = db.session.query(Paragraph).\
            join(ClassificationResult, ClassificationResult.id == Paragraph.classification_result_id).\
            join(Document, Document.id == ClassificationResult.document_id).\
            where(Document.document_name == document_name).\
            all()
        # list = {x.id: x for x in paragraph_list}
        list = []
        for paragraph in paragraph_list:
            tags = []
            for tag in paragraph.paragraph_tags:
                tags.append({'text': tag.label, 'id': tag.id})
            list.append(
                {'classification_id': paragraph.classification_result_id, 'id': paragraph.id, 'key': str(paragraph.id)+"_"+str(paragraph.classification_result_id), 'tag': tags,
                    'paragraph': paragraph.paragraph})

        return list

    def is_document_classification(self, document):
        classification_result = db.session.query(ClassificationResult).\
            join(Document, Document.id == ClassificationResult.document_id).\
            where(Document.id == document.id).\
            first()
        return classification_result

    def save_classification_result(self, document, paragraphs):

        classification = ClassificationResult(
            document_id=document.id,
            status=ClassificationResultStatus.Updated,
        )
        db.session.add(classification)
        db.session.flush()
        # db.session.rollback();
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

    def update_classification_result(self, user, document, table_edit_log):

        classification_result = db.session.query(ClassificationResult).\
            join(Document, Document.id == ClassificationResult.document_id).\
            where(Document.document_name == document.document_name).\
            where(User.id == user.id).\
            first()
        for edit in table_edit_log:
            if(edit.get('type') == 'delete_tag'):
                tag = edit.get('data')
                paragraph_id = edit.get('row_id')
                glossary_tag = db.session.query(ParagraphTag).\
                    join(Paragraph, Paragraph.id == ParagraphTag.paragraph_id).\
                    join(ClassificationResult, ClassificationResult.id == Paragraph.classification_result_id).\
                    where(ClassificationResult.id == classification_result.id).\
                    where(Paragraph.id == paragraph_id).\
                    where(ParagraphTag.label == tag).\
                    first()
                if(glossary_tag):
                    db.session.delete(glossary_tag)

            elif(edit.get('type') == 'add_tag'):
                tag = edit.get('data')
                paragraph_id = edit.get('row_id')
                new_tag = ParagraphTag(
                    label=tag,
                    paragraph_id=paragraph_id
                )
                db.session.add(new_tag)

                if(edit.get('new', None)):
                    paragraph = db.session.query(Paragraph).where(
                        Paragraph.id == paragraph_id).first()
                    training_data = TrainingData(
                        label=tag, paragraph=paragraph.paragraph, user_id=user.id)
                    db.session.add(training_data)

            elif(edit.get('type') == 'delete_row'):
                paragraph_id = edit.get('row_id')
                paragraph_obj = db.session.query(Paragraph).\
                    join(ClassificationResult, ClassificationResult.id == Paragraph.classification_result_id).\
                    where(ClassificationResult.id == classification_result.id).\
                    where(Paragraph.id == paragraph_id).\
                    first()
                if(paragraph_obj):
                    db.session.delete(paragraph_obj)

        db.session.commit()
        return True

    def classify_paragraph(self, paragraph):
        paragraph_tags = self.fast_text_service.classify_paragraph(
            paragraph.paragraph)
        if(paragraph_tags):
            for tag in paragraph_tags[0][0]:
                new_tag = ParagraphTag(
                    label=tag.split('__label__')[1],
                    paragraph_id=paragraph.id
                )
                db.session.add(new_tag)
        return True
