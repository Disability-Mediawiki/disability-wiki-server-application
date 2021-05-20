

import logging
import os

import fitz
from application.main.model.Document import Document
from application.main.model.Enum.DocumentStatus import DocumentStatus
from application.main.model.User import User
from application.main.service.AuthService import AuthService
from application.main.service.WikibaseApi import WikibaseApi
from flask import Flask, current_app, jsonify, request
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .. import db


class PdfService():
    def __init__(self):
        self.auth_service = AuthService()

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
