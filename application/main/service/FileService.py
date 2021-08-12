

from application.main.model.Enum.DocumentType import DocumentType
from application.main.model.Paragraph import Paragraph
from flask_restful import Resource, reqparse, reqparse
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import Flask, request, jsonify, current_app
from flask_restplus import Resource, Api, Namespace

from .. import db
from application.main.model.User import User
from application.main.model.Document import Document
from application.main.model.Enum.DocumentStatus import DocumentStatus
# from threading import Thread
from application.main.service.WikibaseApi import WikibaseApi
from application.main.service.AuthService import AuthService
from application.main.service.PdfService import PdfService
from application.main.service.DocumentClassificationService import DocumentClassificationService
from application.main.service.PublisherService import PublisherService


class FileService():
    def __init__(self):
        self.auth_service = AuthService()
        self.pdf_service = PdfService()
        self.document_classification_service = DocumentClassificationService()
        self.publisher = PublisherService()

    def upload_file(self, filename, language, description, country, file, user):
        try:
            document = Document(
                document_name=filename,
                user_id=user.id,
                status=DocumentStatus.Processing,
                document_type=DocumentType.Document,
                language=language,
                description=description
            )
            db.session.add(document)
            db.session.commit()
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))

            paragraphs = self.pdf_service.extract_paragraph(filename)
            if(paragraphs):
                self.save_paragraph(document, paragraphs)
            document.status = DocumentStatus.Classified
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def upload_file_async(self, filename, language, description, country, file, user):
        try:
            document = Document(
                document_name=filename,
                user_id=user.id,
                status=DocumentStatus.Processing,
                document_type=DocumentType.Document,
                language=language,
                description=description
            )
            db.session.add(document)
            db.session.commit()
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))
            self.publisher.publish_document_extraction(document)
            # job = Thread(target=self.extract_document,
            #              kwargs=document)
            # job.start()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def get_document(self, document, user):
        document = Document.query.filter_by(
            id=document.get('id'),
            user_id=user.id
        ).first()
        if(document):
            return document
        else:
            return False

    def is_name_exit(self, name):
        search = "%{}%".format(name.rstrip().lstrip())
        # document = Document.query.filter_by(
        #     document_name=name
        # ).first()
        document = Document.query.filter(
            Document.document_name.like(search)
        ).all()
        if(document):
            return True
        else:
            return False

    def get_document_by_doc_id_and_user(self, document_id, user):
        document = Document.query.filter_by(
            id=document_id,
            user_id=user.id
        ).first()
        if(document):
            return document
        else:
            return False

    def get_document_by_id(self, document_id):
        document = Document.query.filter_by(
            id=document_id
        ).first()
        if(document):
            return document
        else:
            return False

    def get_all_document(self, user):
        document_list = db.session.query(Document).\
            join(User, Document.user_id == User.id).\
            where(Document.user_id == user.id).all()
        if(len(document_list) > 0):
            result = []
            for doc in document_list:
                result.append({'id': doc.id, 'name': doc.document_name, 'type': doc.document_type.value,
                              'status': doc.status.value, 'date': doc.uploaded_on, 'key': doc.id, 'link': doc.document_link})
            return result
        else:
            return False

    def get_all_pending_document(self, user):
        document_list = db.session.query(Document).\
            join(User, Document.user_id == User.id).\
            where(Document.user_id == user.id).\
            filter(Document.status.in_([DocumentStatus.Processing, DocumentStatus.Classified])).\
            all()
        # filter(Document.status == DocumentStatus.Processing or Document.status ==
        #        DocumentStatus.Classified).all()

        if(len(document_list) > 0):
            result = []
            for doc in document_list:
                result.append({'id': doc.id, 'name': doc.document_name, 'type': doc.document_type.value,
                              'status': doc.status.value, 'date': doc.uploaded_on, 'key': doc.id})
            return result
        else:
            return False
