
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt
from .Enum import DocumentStatus


class Synonym(db.Model):
    """ Synonym Model"""
    __tablename__ = "synonym"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(255), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    glossary_tag_id = Column(Integer, ForeignKey('glossary_tag.id'))

    glossary_tag = relationship("GlossaryTag", back_populates="synonyms")

    def __init__(self, label, glossary_tag_id):
        self.label = label
        self.glossary_tag_id = glossary_tag_id
        self.created_on = datetime.datetime.now()
