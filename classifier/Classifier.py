# from DbConnector import DbConnector

from DbConnector import DbConnector
from PdfExtractor import Tree
from sqlalchemy import text
from sqlalchemy import create_engine


class Classifier():
    def __init__(self):
        ""
        db = DbConnector()
        pdf_extractor = Tree()
        self.engine = db.create_db_engine()

    def classify(self):
        result = self.engine.execute(
            text(
                "SELECT * FROM dis_wiki.document;"
            )
        )
        for item in result:
            print(item)


classifier = Classifier()
classifier.classify()
