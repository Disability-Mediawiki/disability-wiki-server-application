
from application.main.model.TrainingData import TrainingData
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
import json
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from .. import db
from application.main.component.FastTextModelComponent import FastTextModelComponent


class FastTextService():
    def __init__(self):
        self.fast_text_component = FastTextModelComponent()
        self.model = self.fast_text_component.load_model()

    def create_model(self, filename):
        self.fast_text_component.create_model(filename)
        return True

    def classify_paragraph(self, text):
        texts = [text]
        labels = self.model.predict(texts, k=5)
        if(labels and len(labels) > 0):
            return labels
        else:
            return False
