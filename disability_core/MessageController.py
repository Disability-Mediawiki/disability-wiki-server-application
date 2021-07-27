from application.main.service.enum.MesssageQueue import MesssageQueue
import os
import pika
# from .service.DocumentClassification import callback
from .service.MessageService import MessageService
from application.main import db
from application.main.model.Paragraph import Paragraph


class MessageController():
    def __init__(self):
        ""
        self.message_service = MessageService()

    def run(self):
        sleepTime = 10
        print(' [*] Sleeping for ', sleepTime, ' seconds.')
        # time.sleep(10)
        print(' [*] Connecting to server ...')
        # connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(
            queue=MesssageQueue.DOCUMENT_EXTRACTION.value, durable=True)
        channel.queue_declare(
            queue=MesssageQueue.UPLOAD_WIKIBASE.value, durable=True)
        print('CORE WORKER STARTED')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=MesssageQueue.DOCUMENT_EXTRACTION.value,
                              on_message_callback=self.message_service.extract_document)
        channel.basic_consume(queue=MesssageQueue.UPLOAD_WIKIBASE.value,
                              on_message_callback=self.message_service.upload_wikibase)
        channel.start_consuming()
