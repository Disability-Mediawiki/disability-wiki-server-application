
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt


class ParagraphTag(db.Model):
    """ParagraphTag Model"""
    __tablename__ = "paragraph_tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_on = db.Column(db.DateTime, nullable=False)
    label = db.Column(db.String(255), unique=False, nullable=False)
    paragraph_id = Column(
        Integer, ForeignKey('paragraph.id'),  nullable=False)
    paragraph = relationship(
        "Paragraph", back_populates="paragraph_tags")

    def __init__(self, label, paragraph_id):
        self.label = label
        self.paragraph_id = paragraph_id
        self.created_on = datetime.datetime.now()
