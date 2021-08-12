

from application.main.model.Enum.DocumentType import DocumentType
import logging
import os
from threading import Thread

from application import db
from application.main.model.Document import Document

from application.main.model.Enum.DocumentStatus import DocumentStatus
from application.main.model.Paragraph import Paragraph
from application.main.model.User import User
from application.main.service.AuthService import AuthService
from application.main.service.PdfService import PdfService
from application.main.service.PublisherService import PublisherService
from application.main.service.WikibaseApi import WikibaseApi
from flask import Flask, current_app, jsonify, request
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .DocumentClassificationService import DocumentClassificationService


class FileService():
    def __init__(self):
        self.pdf_service = PdfService()
        self.document_classification_service = DocumentClassificationService()
        self.publisher = PublisherService()

    def extract_document(self, doc):
        try:
            document = Document.query.filter_by(
                id=doc.get('id'),
            ).first()
            if(document):
                if(document.document_type == DocumentType.Document):
                    paragraphs = self.pdf_service.extract_paragraph(
                        document.document_name)
                    if(paragraphs):
                        self.save_paragraph(document, paragraphs)
                    document.status = DocumentStatus.Classified
                    db.session.commit()
                    return True
                elif(document.document_type == DocumentType.WebContent):
                    paragraphs = db.session.query(Paragraph).\
                        join(Document, Document.id == Paragraph.document_id).\
                        where(Document.id == document.id).\
                        all()
                    for pr in paragraphs:
                        self.document_classification_service.classify_paragraph(
                            pr)
                    document.status = DocumentStatus.Classified
                    db.session.commit()
                    return True

            else:
                return False
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    def save_paragraph(self, document, paragraphs):
        try:
            # db.session.rollback();
            count = 1
            for paragraph in paragraphs:
                pr = Paragraph(
                    label=document.document_name.split(
                        '.')[0]+" paragraph " + str(count),
                    paragraph=paragraph,
                    document_id=document.id
                )
                db.session.add(pr)
                db.session.commit()
                self.document_classification_service.classify_paragraph(pr)
                count += 1
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
