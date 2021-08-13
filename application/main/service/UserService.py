

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
        try:
            user = User(
                email='test@test.com',
                password='test'
            )
            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token(user.id)
            return auth_token
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def register_user(self, username, email, password):
        try:
            user = User(
                user_name=username,
                email=email,
                password=password
            )
            db.session.add(user)
            db.session.commit()
            # auth_token = user.encode_auth_token(user.id)
            return user
        except Exception as e:
            print(e)
            db.session.rollback()
            raise

    def get_user(self, email):
        # user = User.query.filter_by(
        #     email=email
        # ).first()
        user = db.session.query(User).filter_by(
            email=email
        ).first()
        return user

    def get_user_by_id(self, id):
        # user = User.query.get(id)
        user = db.session.query(User).filter_by(
            id=id
        ).first()
        return user

    def is_admin_user(self, id):
        # user = User.query.filter_by(
        #     id=id
        # ).first()
        user = db.session.query(User).filter_by(
            id=id
        ).first()
        if(user and user.admin):
            return user
        else:
            return False

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

    def logout(self, auth_token):
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            try:
                blacklist_token = self.auth_service.blacklist_token(
                    auth_token)
                return True
            except Exception as e:
                print(e)
                return False
