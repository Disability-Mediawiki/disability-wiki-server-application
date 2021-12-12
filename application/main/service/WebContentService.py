

from application.main.model.Enum.DocumentType import DocumentType
from application.main.model.Paragraph import Paragraph
from flask_restful import Resource, reqparse, reqparse
import os
import re
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import Flask, request, jsonify, current_app
from flask_restplus import Resource, Api, Namespace
import requests
from bs4 import BeautifulSoup


from .. import db
from application.main.model.User import User
from application.main.model.Document import Document
from application.main.model.Enum.DocumentStatus import DocumentStatus
# from threading import Thread
from application.main.service.AuthService import AuthService
from application.main.service.PdfService import PdfService
from application.main.service.DocumentClassificationService import DocumentClassificationService
from application.main.service.PublisherService import PublisherService


class WebContentService():
    def __init__(self):
        self.auth_service = AuthService()
        self.pdf_service = PdfService()
        self.document_classification_service = DocumentClassificationService()
        self.publisher = PublisherService()
        

    def upload_web_content(self, filename, language, description, country, paragraphs, link, user):
        try:
            document = Document(
                document_name=filename,
                user_id=user.id,
                status=DocumentStatus.Processing,
                document_type=DocumentType.WebContent,
                language=language,
                description=description,
                document_link=link
            )
            db.session.add(document)
            db.session.commit()
            if(paragraphs):
                self.save_paragraph(document, paragraphs)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def save_paragraph(self, document, paragraphs):
        try:
            count = 1
            for paragraph in paragraphs:
                if paragraph:
                    pr = Paragraph(
                        label=document.document_name+"_paragraph_" + str(count),
                        paragraph=re.sub(
                            '\?|\#|\!|\/|\;|\:|\$', '', paragraph.get('text').replace("\n", " ").rstrip().lstrip()),
                        document_id=document.id
                    )
                    db.session.add(pr)
                    count += 1
            db.session.commit()
            self.publisher.publish_document_extraction(document)
            
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    # /*
    # SCRAP THE WEBSITE AND GET ALL PARAGRAPHS AND HYBERLINKS
    # */
    def browse_and_scrape(self, url):
        formatted_url = url
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
            }
            html_text = requests.get(formatted_url, headers=headers).text
            soup = BeautifulSoup(html_text, "html.parser")
            print(f"Now Scraping - {formatted_url}")

            paragraphs = soup.find_all("p")
            result = []
            count = 0
            for p in paragraphs:
                # get all hyper link
                links = []
                for a in p("a"):
                    links.append({'text': a.text, 'link': a.get('href')})
                result.append({'id': count, 'text': p.text, 'links': links})
                count += 1
            return result
        except Exception as e:
            print(e)
            return False
