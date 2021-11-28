
import os
import pika
import time
import json
from application.main import db
from application.main.model.Paragraph import Paragraph
from .FileService import FileService
from .UploadRequestService import UploadRequestService


class MessageService():
    def __init__(self):
        ""
        self.file_service = FileService()
        self.wikbase_service = UploadRequestService()

    def extract_document(self, ch, method, properties, body):
        print(" Extracting document %s" % body)
        cmd = body.decode()
        if(cmd != None):
            document = json.loads(cmd)
            self.file_service.extract_document(document)
        print("COMPLETED: Document extracted %s" % body)
        db.session.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def upload_wikibase(self, ch, method, properties, body):
        print(" UPLOADING TO WIKIBASE %s" % body)
        cmd = body.decode()
        if(cmd != None):
            payload = json.loads(cmd)
            self.wikbase_service.upload_to_wikibase(payload)
        print("COMPLETED: UPLOAD TO WIKIBASE %s" % body)
        db.session.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)
