from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import datetime

from ..models.auth import UserModel
from ..utility.validators import json_checker, login_checker, registration_checker

users_bp = Blueprint('users', __name__, url_prefix='/api/v1')

user_model = UserModel()

class Users(object):
    @users_bp.route("/login", methods=["POST"])
    def user_login():
        checks = login_checker(request)
        if checks:
            return make_response(jsonify({
                "status":"not acceptable",
                "message":checks
                }), 406)

        data = request.get_json()
        email = data['email']
        password = data['password']

        user = user_model.get_user_by_email(email)
        if not user:
            return make_response(jsonify({
                "status": "not found",
                "message": "User does not exist"
            }), 404)

        credentials = user_model.access_token(email, password)
        if credentials:
            return make_response(jsonify({
                "status": "user logged in",
                "username": user['username'],
                "login": True,
                "token": credentials
                }), 200)

        else:
            return make_response(jsonify({
                "status": "login error",
                "login": False
                }), 401)
