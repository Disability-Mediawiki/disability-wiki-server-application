
import datetime
from flask import current_app
from .. import db, flask_bcrypt as bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, Enum, ForeignKey
from .Enum import DocumentStatus


class Country(db.Model):
    """ Country Model"""
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False)

    documents = relationship("Document", back_populates="country")

    def __init__(self, name):
        self.name = name
        self.requested_on = datetime.datetime.now()
