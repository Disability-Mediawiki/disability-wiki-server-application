
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt


class Paragraph(db.Model):
    """Paragraph Model"""
    __tablename__ = "paragraph"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, nullable=False)
    paragraph = db.Column(db.TEXT(4294000000), unique=False, nullable=False)
    label = db.Column(db.String(255), unique=False, nullable=False)
    document_id = Column(
        Integer, ForeignKey('document.id'),  nullable=False)
    document = relationship(
        "Document", back_populates="paragraphs")
    paragraph_tags = relationship(
        "ParagraphTag", cascade="all,delete", back_populates="paragraph")

    def __init__(self, label, paragraph, document_id):
        self.label = label
        self.paragraph = paragraph
        self.document_id = document_id
        self.created_on = datetime.datetime.now()
