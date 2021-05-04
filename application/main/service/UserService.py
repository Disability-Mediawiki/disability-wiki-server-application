

from flask_restful import Resource, reqparse, reqparse
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import logging
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api, Namespace
from flask import current_app

from application.main.model.User import User
from .. import db, flask_bcrypt

from application.main.service.WikibaseApi import WikibaseApi
from application.main.service.AuthService import AuthService


class UserService():
    def __init__(self):
        self.auth_service = AuthService()

    def create_user(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        return auth_token

    def register_user(self, username, email, password):
        user = User(
            user_name=username,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        return auth_token

    def get_user(self, email):
        user = User.query.filter_by(
            email=email
        ).first()
        return user

    def login(self, user, password):
        if self.auth_service.validate_password(
            user.password, password
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                return auth_token
            else:
                return None
        else:
            return None
