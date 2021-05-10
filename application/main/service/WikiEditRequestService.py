
# Pywikibot
import json
import logging
import os

from application.main.model.User import User
from flask import Flask, current_app, jsonify, request
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from application.main.model.UploadRequest import UploadRequest
from application.main.service.FileService import FileService
from .. import db


class WikiEditRequestService():
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.file_service = FileService()

    def create_upload_request(self, file_name, user):
        if(self.file_service.move_file_wiki_upload_request(file_name)):
            upload_request = UploadRequest(
                file_name=file_name,
                user_id=user.id
            )
            db.session.add(upload_request)
            db.session.commit()
            return True
        else:
            return False
