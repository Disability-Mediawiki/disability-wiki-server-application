from functools import wraps

import jwt
from flask import Blueprint, Flask, request, current_app
from flask_restplus import Api, Resource, fields
from application.main.service.AuthService import AuthService
from application.main.model.User import BlacklistToken
from application.main.service.UserService import UserService

# def token_authenticate(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):

#         token = None

#         if 'X-API-KEY' in request.headers:
#             token = request.headers['X-API-KEY']

#         if not token:
#             return {'message': 'Token is missing.'}, 401

#         if token != 'mytoken':
#             return {'message': 'Your token is wrong, wrong, wrong!!!'}, 401

#         print('TOKEN: {}'.format(token))
#         return f(*args, **kwargs)

#     return decorated


def token_authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_token = None

        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]

        if not auth_token:
            return {'message': 'Token is missing.'}, 401

        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                # return payload['sub']
                print('TOKEN: {}'.format(auth_token))
                return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

        # print('TOKEN: {}'.format(auth_token))
        # return f(*args, **kwargs)

    return decorated


def token_authenticate_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_token = None

        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]

        if not auth_token:
            return {'message': 'Token is missing.'}, 401

        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                # return payload['sub']
                user_service = UserService()
                user = user_service.is_admin_user(payload['sub'])
                if(user):
                    print('TOKEN: {}'.format(auth_token))
                    return f(*args, **kwargs)
                else:
                    return {'message': 'Unauthorized'}, 401
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

        # print('TOKEN: {}'.format(auth_token))
        # return f(*args, **kwargs)

    return decorated
