import pika
from flask import current_app
from application.main.service.enum.MesssageQueue import MesssageQueue
import json


class PublisherService():
    def __init__(self):
        ""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=current_app.config['MESSAGING_SERVICE_HOST']))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=MesssageQueue.DOCUMENT_CLASSIFICATION.value,
                                   durable=True)
        self.channel.queue_declare(queue=MesssageQueue.DOCUMENT_EXTRACTION.value,
                                   durable=True)
        self.channel.queue_declare(queue=MesssageQueue.UPLOAD_WIKIBASE.value,
                                   durable=True)

    def publish_document_classification(self, document):
        body = json.dumps(document)
        self.channel.basic_publish(
            exchange='',
            routing_key=MesssageQueue.DOCUMENT_CLASSIFICATION.value,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        self.connection.close()

    def publish_document_extraction(self, doc):
        body = json.dumps({'id': doc.id, 'name': doc.document_name,
                           'status': doc.status.value, 'key': doc.id})
        self.channel.basic_publish(
            exchange='',
            routing_key=MesssageQueue.DOCUMENT_EXTRACTION.value,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        self.connection.close()

    def publish_wikibase_upload(self, url, document_id, request_id):
        body = json.dumps(
            {'url': url, 'document_id': document_id, 'request_id': request_id})
        self.channel.basic_publish(
            exchange='',
            routing_key=MesssageQueue.UPLOAD_WIKIBASE.value,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        self.connection.close()
