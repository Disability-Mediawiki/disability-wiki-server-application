

import datetime
from flask import current_app
from .. import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

# basic model


class UploadRequest(db.Model):
    """ Upload Request Model """
    __tablename__ = "upload_request"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), unique=True, nullable=False)
    requested_on = db.Column(db.DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="upload_requests")

    def __init__(self, file_name, user_id):
        self.file_name = file_name
        self.requested_on = datetime.datetime.now()
        self.user_id = user_id
