# /*
# MANAGE UPLOAD REQUEST TO WIKIBASE
# EACH UPLOAD REQUEST ARE STAGGED AND VERRIFIED BY ADMIN USERS {ACCEPT OR REJECT}
# */

from application.main.model.Enum.DocumentType import DocumentType
from application.main.service.PublisherService import PublisherService
import json
import logging
import os
import re

from application.main.model.Enum.DocumentStatus import DocumentStatus
from application.main.model.Paragraph import Paragraph
from application.main.model.Enum.WikiEditReqestStatus import WikieditRequestStatus
from application.main.model.Document import Document

from application.main.model.User import User
from flask import Flask, current_app, jsonify, request
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from application.main.model.UploadRequest import UploadRequest
from application.main.service.FileService import FileService
from .. import db

import urllib.parse

class UploadRequestService():
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()
        self.messaging_service = PublisherService()
  
    def create_wikiedit_upload_request(self, user, document):
        try:
            upload_request = UploadRequest(
                user_id=user.id,
                document_id=document.id,
            )
            db.session.add(upload_request)
            document.status = DocumentStatus.Requested
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

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

    def update_wikiedit_request_async(self, document, request_id, status):
        try:
            upload_request = db.session.query(UploadRequest).\
                where(UploadRequest.id == request_id).\
                where(UploadRequest.document_id == document.id).\
                where(UploadRequest.status == WikieditRequestStatus.Pending).\
                first()
            if(upload_request):
                if(status == WikieditRequestStatus.Accepted.value):
                    upload_request.status = WikieditRequestStatus.Uploading
                    db.session.commit()
                    url = request.host_url
                    file_url = ""
                    if(document.document_type == DocumentType.Document):
                        parsed_name = urllib.parse.quote_plus(
                            document.document_name)
                        file_url = f"{url}api/file/download-document?file_name={parsed_name}"
                    else:
                        file_url = document.document_link

                    self.messaging_service.publish_wikibase_upload(
                        file_url, document.id, request_id)
                    return True

                elif(status == WikieditRequestStatus.Rejected.value):

                    upload_request.status = WikieditRequestStatus.Rejected
                    document.status = DocumentStatus.Deleted
                    db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            db.session.rollback()
            raise
