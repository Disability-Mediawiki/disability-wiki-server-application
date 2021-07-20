
from application.main.model.TrainingData import TrainingData
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
import json
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app
from .CeleryService import celery
from celery.utils.log import get_task_logger
import os


class AsyncService():
    def __init__(self):

        self.logger = get_task_logger(__name__)

    @celery.task(bind=True)
    # @celery.task
    def task(self):
        file1 = open(os.path.join(
            './resources/'), 'w')
        file1.writelines("working from celelry")
        file1.close()
        self.info('test logger working')
        return "test reulsflkdsjafsklaflkjasdljsdlkafjlk;sjfdlkjsdflkj"
