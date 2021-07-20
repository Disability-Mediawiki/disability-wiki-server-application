

from application.main.model.Enum.TrainingDataStatus import TrainingDataStatus
from application.main.model.User import User
import logging
import os

from application.main.model.TrainingData import TrainingData
from flask import current_app, jsonify, request
from flask_restful import Resource, reqparse
from flask_restplus import Api, Namespace, Resource

from .. import db, flask_bcrypt


class TrainingService():
    def __init__(self):
        ""

    def get_training_data(self, user):
        training_data = db.session.query(TrainingData).\
            join(User, User.id == TrainingData.user_id).\
            filter(TrainingData.status == TrainingDataStatus.Pending).\
            all()

        list = []
        for data in training_data:
            list.append({'id': data.id, 'tag': data.label,
                        'paragraph': data.paragraph, 'status': data.status.value, 'key': str(data.id)+'_td_key'})
        return list

    def train_model(self, training_data):
        ""
        return True
