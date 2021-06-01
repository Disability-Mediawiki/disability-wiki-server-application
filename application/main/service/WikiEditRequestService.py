
# Pywikibot
from application.main.model.Paragraph import Paragraph
from application.main.service.WikibaseApi import WikibaseApi
from application.main.model.Enum.WikiEditReqestStatus import WikieditRequestStatus
from application.main.model.Document import Document
from application.main.model.ClassificationResult import ClassificationResult
import json
import logging
import os
import re
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
from application.main.service.LoggerService import LoggerService
from .. import db


class WikiEditRequestService():
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        self.wikibase_api = WikibaseApi()
        self.logger_service = LoggerService()

    def create_upload_request(self, file_name, user):
        if(self.file_service.move_file_wiki_upload_request(file_name)):
            upload_request = UploadRequest(
                file_name=file_name,
                user_id=user.id
            )
            db.session.add(upload_request)
            db.session.commit()
            return True
        else:
            return False

    def create_wikiedit_upload_request(self, user, document):
        classification_result = db.session.query(ClassificationResult).\
            join(Document, Document.id == ClassificationResult.document_id).\
            where(Document.document_name == document.document_name).\
            where(User.id == user.id).\
            first()
        upload_request = UploadRequest(
            user_id=user.id,
            document_id=document.id,
            classification_result_id=classification_result.id
        )
        db.session.add(upload_request)
        db.session.commit()
        return True

    def get_all_pending_request(self):
        upload_request = db.session.query(UploadRequest).\
            filter((UploadRequest.status == WikieditRequestStatus.Pending) | (UploadRequest.status == WikieditRequestStatus.Uploading)).\
            all()
        # where(UploadRequest.status == WikieditRequestStatus.Pending) OR (UploadRequest.status == WikieditRequestStatus.Uploading).\

        if(len(upload_request) > 0):
            result = []
            for request in upload_request:
                result.append({'id': request.id, 'date': request.requested_on,
                               'status': request.status.value,
                               'user_name': request.user.user_name, 'user_id': request.user_id,
                               'document_name': request.document.document_name, 'document_id': request.document_id})
            return result
        else:
            return False

    def update_wikiedit_request(self, document, request_id, status):
        upload_request = db.session.query(UploadRequest).\
            where(UploadRequest.id == request_id).\
            where(UploadRequest.document_id == document.id).\
            where(UploadRequest.status == WikieditRequestStatus.Uploading).\
            one()
        if(upload_request):
            if(status == WikieditRequestStatus.Accepted.value):
                "MAKE THE PYWIKI UYPLOAD"
                upload_request.status = WikieditRequestStatus.Uploading
                db.session.commit()
                # insert document

                url = request.host_url
                document_name = document.document_name.split('.')[0]
                label = {document.language.value: document_name.capitalize()}
                description = {
                    document.language.value: document.description.capitalize()}
                wiki_doc_item = self.wikibase_api.create_document_entity(
                    label, description, document_name,
                    f"{url}api/file/download-document?file_name={document.document_name}")
                # http://localhost:5000/api/file/download-document?file_name=CRPD.pdf

                if(not wiki_doc_item):
                    return False

                # INSERT PARAGRAPH
                paragraphs = db.session.query(Paragraph).\
                    join(ClassificationResult, ClassificationResult.id == Paragraph.classification_result_id).\
                    join(Document, Document.id == ClassificationResult.document_id).\
                    where(Document.id == document.id).\
                    all()

                count = 0
                for paragraph in paragraphs:
                    if(count < 4):
                        count += 1
                        continue
                    paragraph_label = {
                        document.language.value: document_name.capitalize()+" "+paragraph.label.capitalize()}
                    paragraph_description = {
                        document.language.value: f"Paragraph from {document.document_name} document"}
                    try:
                        paragraph_text = paragraph.paragraph.rstrip().replace('\n', ' ').replace('\t', ' ')
                        paragraph_text = re.sub(
                            '\ |\/|\;|\:|\]|\[|\{|\}|\?|\*|\&|\@|\<|\>', ' ', paragraph_text)
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

                return True

            elif(status == WikieditRequestStatus.Rejected.value):
                upload_request.status = WikieditRequestStatus.Rejected
                db.session.commit()
            return True
        else:
            return False
