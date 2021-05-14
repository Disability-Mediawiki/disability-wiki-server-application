
import datetime
from flask import current_app
from .. import db, flask_bcrypt as bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, Enum, ForeignKey
from .Enum import DocumentStatus


class Document(db.Model):
    """ Document Model"""
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_name = db.Column(db.String(255), unique=False, nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum(DocumentStatus), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="documents")

    def __init__(self, document_name, user_id):
        self.document_name = document_name
        self.requested_on = datetime.datetime.now()
        self.user_id = user_id
