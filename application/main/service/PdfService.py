

import logging
import os
import uuid

import fitz
from application.main.model.Document import Document
# from application.main.model.Enum.DocumentStatus import DocumentStatus
from application.main.model.User import User
# from application.main.service.AuthService import AuthService
# from application.main.service.WikibaseApi import WikibaseApi

# from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.utils import secure_filename
from flask import (Flask, current_app, send_file, send_from_directory)
from .. import db
from application.main.service.ParagraphExtractorService import ParagraphParser


class PdfService():
    def __init__(self):
        ""
        self.paragraph_extraction = ParagraphParser()

    def extract_paragraph(self, file_name):
        try:
            results = self.paragraph_extraction.pdfParagraphExtractor(
                current_app.config['UPLOAD_FOLDER']+'/'+file_name)
            if(results):
                return results
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def text_search_and_highligh(self, file_name, text):
        doc = fitz.open(current_app.config['UPLOAD_FOLDER']+'/'+file_name)

        # doc = fitz.open(
        #     os.path.join(CACHE_FOLDER, str(request_args["user_id"]), request_args["index_name"],
        #                  request_args["filename"]))
        pool = []
        for index, page in enumerate(doc):
            # Search for answer_text
            answer_occurrences = page.searchFor(text, quads=True)
            if len(answer_occurrences) != 0:
                pool.append(index)
            # Highlight all the occurrence
            for occ_ans in answer_occurrences:
                ans_annot = page.addHighlightAnnot(occ_ans)
                ans_annot.set_colors(stroke=(253 / 255, 202 / 255, 64 / 255))
                ans_annot.update()
        new_doc = fitz.open()
        for pageNumber in pool:
            new_doc.insertPDF(doc, from_page=pageNumber, to_page=pageNumber)

        # new_doc.save(os.path.join(
        #     current_app.config['UPLOAD_FOLDER'], 'output.pdf'), garbage=4, deflate=True, clean=True)

        os.makedirs(os.path.join(
            current_app.config['TEMP_DOC_FOLDER'], "tmp"), exist_ok=True)
        temp_path = os.path.join(
            current_app.config['TEMP_DOC_FOLDER'], 'tmp', str(uuid.uuid4()) + '.pdf')
        new_doc.save(temp_path, garbage=4, deflate=True, clean=True)
        return send_file(temp_path, as_attachment=False)

    def test_highlight(self):
        doc = fitz.open(current_app.config['UPLOAD_FOLDER']+'/CVLJ.pdf')
        for page in doc:
            # SEARCH
            text = "Dear Hiring Manager"
            text_instances = page.searchFor(text)

            # HIGHLIGHT
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
                highlight.update()
        doc.save(os.path.join(
            current_app.config['UPLOAD_FOLDER'], 'output.pdf'), garbage=4, deflate=True, clean=True)
