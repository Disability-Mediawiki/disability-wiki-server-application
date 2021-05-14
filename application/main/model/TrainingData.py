
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt
from .Enum import DocumentStatus


class TrainingData(db.Model):
    """ Training Data Model"""
    __tablename__ = "training_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(255), unique=False, nullable=False)
    paragraph = db.Column(db.String(255), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="training_sets")

    def __init__(self, label, paragraph, user_id):
        self.label = label
        self.paragraph = paragraph
        self.created_on = datetime.datetime.now()
        self.user_id = user_id
