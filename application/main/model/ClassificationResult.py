
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt
from .Enum import DocumentStatus
from .Enum.ClassificationResultStatus import ClassificationResultStatus


class ClassificationResult(db.Model):
    """Classification Result Model"""
    __tablename__ = "classification_result"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # label = db.Column(db.String(255), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum(ClassificationResultStatus), nullable=False)
    updated_on = db.Column(db.DateTime, nullable=True)

    document_id = Column(Integer, ForeignKey('document.id'),  nullable=True)
    document = relationship("Document", back_populates="classification_result")

    paragraphs = relationship(
        "Paragraph", back_populates="classification_result")

    def __init__(self, document_id, status, updated_on=None):

        self.document_id = document_id
        self.created_on = datetime.datetime.now()
        if(updated_on):
            self.updated_on = updated_on
        self.status = status
