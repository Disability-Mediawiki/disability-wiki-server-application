
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
from application.main.model.Paragraph import Paragraph
from application.main.model.ParagraphTag import ParagraphTag
from application.main.model.Document import Document
from application.main.model.User import User


class DocumentClassificationService():
    def __init__(self):
        self.fast_text_service = None

    def get_all_paragraphs_and_tags_by_user(self, document_name, document_id, user):
        paragraph_list = db.session.query(Paragraph).\
            join(Document, Document.id == Paragraph.document_id).\
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
                {'document_id': paragraph.document_id, 'id': paragraph.id, 'key': str(paragraph.id)+"_"+str(paragraph.document_id), 'tag': tags,
                 'paragraph': paragraph.paragraph})
        return list

    def get_all_paragraphs_and_tags(self, document_name, document_id):
        paragraph_list = db.session.query(Paragraph).\
            join(Document, Document.id == Paragraph.document_id).\
            where(Document.id == document_id).\
            where(Document.document_name == document_name).\
            all()
        # list = {x.id: x for x in paragraph_list}
        list = []
        for paragraph in paragraph_list:
            tags = []
            for tag in paragraph.paragraph_tags:
                tags.append({'text': tag.label, 'id': tag.id})
            list.append(
                {'document_id': paragraph.document_id, 'id': paragraph.id, 'key': str(paragraph.id)+"_"+str(paragraph.document_id), 'tag': tags,
                    'paragraph': paragraph.paragraph})

        return list

    def is_document_classification(self, document):
        paragraph = db.session.query(Paragraph).\
            join(Document, Document.id == Paragraph.document_id).\
            where(Document.id == document.id).\
            first()
        return paragraph

    def save_classification_result(self, document, paragraphs):

        try:
            count = 1
            for paragraph in paragraphs:
                pr = Paragraph(
                    label=document.document_name+" paragraph " + str(count),
                    paragraph=paragraph.get('paragraph'),
                    document_id=document.id
                )
                db.session.add(pr)
                # db.session.flush()
                db.session.commit()
                for tag in paragraph.get('tags'):
                    p_tag = ParagraphTag(
                        label=tag.get('text'),
                        paragraph_id=pr.id
                    )
                    db.session.add(p_tag)
                count += 1

            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def update_classification_result(self, user, document, table_edit_log):
        try:
            for edit in table_edit_log:
                if(edit.get('type') == 'delete_tag'):
                    tag = edit.get('data')
                    paragraph_id = edit.get('row_id')
                    glossary_tag = db.session.query(ParagraphTag).\
                        join(Paragraph, Paragraph.id == ParagraphTag.paragraph_id).\
                        join(Document, Document.id == Paragraph.document_id).\
                        where(Document.id == document.id).\
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
                        join(Document, Document.id == Paragraph.document_id).\
                        where(Document.id == document.id).\
                        where(Paragraph.id == paragraph_id).\
                        first()
                    if(paragraph_obj):
                        db.session.delete(paragraph_obj)

            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise
