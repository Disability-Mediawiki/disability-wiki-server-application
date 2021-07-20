
import os
import pika
import time
import json
from application.main import db
from application.main.model.Paragraph import Paragraph
from application.main.service.FileService import FileService


class MessageService():
    def __init__(self):
        ""
        self.file_service = FileService()

    def callback(ch, method, properties, body):
        print(" [x] Received %s" % body)
        paragraph_list = db.session.query(Paragraph).\
            all()
        print(*paragraph_list)
        time.sleep(10)
        cmd = body.decode()
        # doc = fitz.open(os.path.dirname(os.path.abspath(__file__)) +'/resources/uploads/CRPD.pdf')
        if cmd == 'hey':
            print("hey there")
        elif cmd == 'hello':
            print("well hello there")
        else:
            print("sorry i did not understand ", body)

        print(" [x] Done")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def extract_document(self, ch, method, properties, body):
        print(" Extracting document %s" % body)
        time.sleep(10)
        cmd = body.decode()
        if(cmd != None):
            document = json.loads(cmd)
            self.file_service.extract_document(document)
        print(" Document extracted %s" % body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def classify_document(self, ch, method, properties, body):
        print(" [x] Received %s" % body)
        time.sleep(4)
        cmd = body.decode()
        my_dict = json.loads(cmd)
        print(my_dict.get('data'))
        print("hey there")
        print(" [x] Done")

        ch.basic_ack(delivery_tag=method.delivery_tag)
