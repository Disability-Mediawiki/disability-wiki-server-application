# from DbConnector import DbConnector

from DbConnector import DbConnector
from PdfExtractor import ParagraphParser
from sqlalchemy import text
from sqlalchemy import create_engine
import datetime


class Classifier():
    def __init__(self):
        ""
        db = DbConnector()
        self.pdf_extractor = ParagraphParser()
        self.engine = db.create_db_engine()

    def classify(self):
        # result = self.engine.execute(
        #     text(
        #         "SELECT * FROM dis_wiki.document;"
        #     )
        # )
        # for item in result:
        #     print(item)

        # documents = self.engine.execute(
        #     text(
        #         "SELECT * FROM dis_wiki.document WHERE status='Processing';"
        #     )
        # )
        # for item in documents:
        #     print(item)

        paragraphs = self.pdf_extractor.pdfParagraphExtractor(
            "F:/Internship York/Repo/Disability-Media-Wiki/flask/server-flask-restplus/resources/uploads")
        count = 1
        # for paragraph in paragraphs:

        #     query = "INSERT INTO  `dis_wiki`.`document_paragraph` (`label` ,`document_id` ,`text` ,`created_on`) VALUES(%s,%s,%s,%s)"
        #     my_data = ('King', 'Five', 45, datetime.datetime.now())

        #     count+=1

    def insert_paragraph(self, statement, query_data):

        id = self.engine.execute(statement, query_data)
        print("ID of Row Added  = ", id.lastrowid)


classifier = Classifier()
classifier.classify()
