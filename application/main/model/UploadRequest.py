

from flask import current_app
import datetime
from .. import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Enum, Integer, ForeignKey
from application.main.model.Enum.WikiEditReqestStatus import WikieditRequestStatus

# basic model


class UploadRequest(db.Model):
    """ Upload Request Model """
    __tablename__ = "upload_request"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # file_name = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(Enum(WikieditRequestStatus), nullable=False)
    requested_on = db.Column(db.DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="upload_requests")

    document_id = Column(Integer, ForeignKey('document.id'))
    document = relationship("Document", back_populates="upload_requests")

    def __init__(self, user_id, document_id,  status=WikieditRequestStatus.Pending.value):
        self.requested_on = datetime.datetime.now()
        self.user_id = user_id
        self.document_id = document_id
        self.status = status
