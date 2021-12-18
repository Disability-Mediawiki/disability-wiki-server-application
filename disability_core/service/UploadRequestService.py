
# /*
# UPLOAD TO WIKIBASE SERVICE
#
# */
from application.main.service.PublisherService import PublisherService
import json
import logging
import os
import re

from application.main.model.Enum.DocumentStatus import DocumentStatus
from application.main.model.Enum.DocumentType import DocumentType
from application.main.model.Paragraph import Paragraph
from application.main.service.WikibaseApi import WikibaseApi
from application.main.model.Enum.WikiEditReqestStatus import WikieditRequestStatus
from application.main.model.Document import Document

from application.main.model.User import User
from flask import Flask, current_app, jsonify, request
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from application.main.model.UploadRequest import UploadRequest
from application.main.service.FileService import FileService
import sys
import traceback
from application.main.service.DebuggWriter import DebuggWriter
from application import db


class UploadRequestService():
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        self.wikibase_api = WikibaseApi()
        self.logger_service = DebuggWriter()
        self.messaging_service = PublisherService()

    def upload_to_wikibase(self, payload):
        try:
            document = db.session.query(Document).\
                where(Document.id == payload.get('document_id')).\
                first()
            upload_request = db.session.query(UploadRequest).\
                where(UploadRequest.id == payload.get('request_id')).\
                where(UploadRequest.document_id == document.id).\
                first()
            document_name = ""
            if(document.document_type == DocumentType.Document):
                document_name = document.document_name.split('.')[0]
            else:
                document_name = document.document_name

            label = {document.language.value: document_name.capitalize()}
            description = {document.language.value: document.description.capitalize()}

            wiki_doc_item = self.wikibase_api.create_document_entity(
                label, description, document_name, payload.get('url'), document.document_type)

            if(not wiki_doc_item):
                return False
            # INSERT PARAGRAPH
            paragraphs = db.session.query(Paragraph).\
                join(Document, Document.id == Paragraph.document_id).\
                where(Document.id == document.id).\
                all()

            count = 0
            for paragraph in paragraphs:
                # paragraph_label = {
                #     document.language.value: document_name.capitalize()+" "+paragraph.label.capitalize()}
                paragraph_label = {
                    document.language.value: paragraph.label.capitalize().rstrip().lstrip()}
                paragraph_description = {
                    document.language.value: f"Paragraph from {document.document_name} document"}
                try:
                    if(not str.isspace(paragraph.paragraph) and paragraph.paragraph):
                        paragraph_text = paragraph.paragraph.replace(
                            '\n', ' ').replace('\t', ' ').replace('\r', ' ').rstrip().lstrip()
                        paragraph_text = re.sub(
                            '\ |\/|\;|\:|\]|\[|\{|\}|\?|\$|\%|\£|\*|\&|\@|\<|\>', ' ', paragraph_text)
                        paragraph_entity = self.wikibase_api.create_paragraph_entity(
                            paragraph_label, paragraph_description, paragraph_text.rstrip().lstrip(), wiki_doc_item, paragraph.paragraph_tags, document.language.value)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    tb = traceback.extract_tb(exc_tb)[-1]
                    print(
                        f"ERROR : Creating paragraph error. MESSSAGE >> {e}")
                    err_msg = f"ERROR : CREATE_PARAGRAPH.:{type(self).__name__}: MESSSAGE >> {e}"
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    tb = traceback.extract_tb(exc_tb)[-1]
                    err_trace = f"ERROR_TRACE >>>: + {exc_type} , method: {tb[2]} , line-no: {tb[1]}"
                    self.logger_service.logError(
                        type(self).__name__, e, exc_type, exc_obj, exc_tb, tb, err_msg)
                count += 1
            upload_request.status = WikieditRequestStatus.Completed
            document.status = DocumentStatus.Completed
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

