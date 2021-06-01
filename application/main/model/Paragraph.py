
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt
from .Enum import DocumentStatus
from .Enum.ClassificationResultStatus import ClassificationResultStatus


class Paragraph(db.Model):
    """Paragraph Model"""
    __tablename__ = "paragraph"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, nullable=False)
    paragraph = db.Column(db.TEXT(4294000000), unique=False, nullable=False)
    # paragraph = db.Column(db.TEXT(16000000), unique=False, nullable=False)
    label = db.Column(db.String(255), unique=False, nullable=False)
    classification_result_id = Column(
        Integer, ForeignKey('classification_result.id'),  nullable=False)
    classification_result = relationship(
        "ClassificationResult", back_populates="paragraphs")
    paragraph_tags = relationship(
        "ParagraphTag", cascade="all,delete", back_populates="paragraph")

    def __init__(self, label, paragraph,  classification_result_id, document_id):
        self.label = label
        self.paragraph = paragraph
        self.classification_result_id = classification_result_id
        self.document_id = document_id
        self.created_on = datetime.datetime.now()
