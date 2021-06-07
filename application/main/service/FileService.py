

from application.main.model.Enum.ClassificationResultStatus import ClassificationResultStatus
from application.main.model.ClassificationResult import ClassificationResult
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


from application.main.service.WikibaseApi import WikibaseApi
from application.main.service.AuthService import AuthService
from application.main.service.PdfService import PdfService


class FileService():
    def __init__(self):
        self.auth_service = AuthService()
        self.pdf_service = PdfService()

    def move_file_wiki_upload_request(self, file_name):
        try:
            if os.path.isfile(os.path.join(
                    current_app.config['RESULT_FOLDER'], file_name)):
                os.replace(os.path.join(
                    current_app.config['RESULT_FOLDER'], file_name),
                    os.path.join(
                    current_app.config['UPLOAD_WIKIEDIT_REQUEST_FOLDER'], file_name))
                return True
            else:
                return False
        except IOError:
            print("File not accessible")
            return False

    def upload_file(self, filename, language, description, country, file, user):

        document = Document(
            document_name=filename,
            user_id=user.id,
            status=DocumentStatus.Processing,
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

    def save_paragraph(self, document, paragraphs):

        classification = ClassificationResult(
            document_id=document.id,
            status=ClassificationResultStatus.Processing,
        )
        db.session.add(classification)
        db.session.commit()
        # db.session.rollback();
        count = 1
        for paragraph in paragraphs:
            pr = Paragraph(
                label=document.document_name.split(
                    '.')[0]+" paragraph " + str(count),
                paragraph=paragraph,
                classification_result_id=classification.id,
                document_id=document.id
            )
            db.session.add(pr)
            count += 1
        db.session.commit()
        return True

    def get_document(self, filename, user):
        document = Document.query.filter_by(
            document_name=filename,
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
            join(User, Document.user_id == User.id).all()
        if(len(document_list) > 0):
            result = []
            for doc in document_list:
                result.append({'id': doc.id, 'name': doc.document_name,
                              'status': doc.status.value, 'date': doc.uploaded_on, 'key': doc.id})
            return result
        else:
            return False

    def get_all_pending_document(self, user):
        document_list = db.session.query(Document).\
            join(User, Document.user_id == User.id).\
            filter(Document.status == DocumentStatus.Processing or Document.status ==
                   DocumentStatus.Classified).all()
        if(len(document_list) > 0):
            result = []
            for doc in document_list:
                result.append({'id': doc.id, 'name': doc.document_name,
                              'status': doc.status.value, 'date': doc.uploaded_on, 'key': doc.id})
            return result
        else:
            return False
