
import datetime

from flask import current_app
from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from .. import db
from .. import flask_bcrypt as bcrypt
from .Enum import DocumentStatus


class GlossaryTag(db.Model):
    """ Glossary Tag Model"""
    __tablename__ = "glossary_tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(255), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    synonyms = relationship("Synonym", back_populates="glossary_tag")

    def __init__(self, label):
        self.label = label
        self.created_on = datetime.datetime.now()
