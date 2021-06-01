
import datetime
from flask import current_app
from .. import db, flask_bcrypt as bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, Enum, ForeignKey
from .Enum.DocumentStatus import DocumentStatus
from .Enum.DocumentLanguage import DocumentLanguage
from .Country import Country


class Document(db.Model):
    """ Document Model"""
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_name = db.Column(db.String(255), unique=False, nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum(DocumentStatus), nullable=False)
    description = db.Column(db.String(1000), unique=False)
    language = db.Column(Enum(DocumentLanguage), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="documents")

    country_id = Column(Integer, ForeignKey('country.id'),  nullable=True)
    country = relationship("Country", back_populates="documents")
    classification_result = relationship(
        "ClassificationResult", back_populates="document")
    upload_requests = relationship(
        "UploadRequest", cascade="all,delete", back_populates="document")

    def __init__(self, document_name, user_id, status, language=DocumentLanguage.en, description=None,  country_id=None):
        self.document_name = document_name
        self.uploaded_on = datetime.datetime.now()
        self.user_id = user_id
        self.status = status
        if country_id:
            self.country_id = country_id
        if description:
            self.description = description
        else:
            self.description = document_name + " Document"
        self.language = language
