from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import datetime

from ..models.auth import UserModel
from ..utility.validators import json_checker, login_checker, registration_checker

users_bp = Blueprint('users', __name__, url_prefix='/api/v2')

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
        username = user_model.get_user_username_by_email(email)
        if credentials:
            return make_response(jsonify({
                "status": "user logged in",
                "username": username,
                "login": True,
                "token": credentials
                }), 200)

        else:
            return make_response(jsonify({
                "status": "login error",
                "login": False
                }), 401)

    @users_bp.route("/register", methods=["POST"])
    @jwt_required
    def register():
        user_email = get_jwt_identity()
        print(user_email)
        user = user_model.get_user_role_by_email(user_email)
        if not user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "Admin User must be logged in"
                }), 401)
        
        checks = registration_checker(request)
        if checks:
            return make_response(jsonify({
                "status":"not acceptable",
                "message":checks
                }), 406)

        data = request.get_json()
        name = data['name']
        email = data['email']
        usrnm = data['username']
        pswrd = data['password']
        is_admin = False

        user = user_model.get_user_by_email(email)
        if user:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "user already exists"
                }), 406)

        else:
            user = user_model.add_user(name, email, usrnm, pswrd, is_admin)
            users = user_model.get_all()
            return make_response(jsonify({
                "status": "created",
                "user": user,
                "users": users
                }), 201)


    @users_bp.route("/logout")
    @jwt_required
    def logout():
        if session.get('logged_in') or session.get('logged_in_admin'):
            session['logged_in'] = False
            session['logged_in_admin'] = False
            return make_response(jsonify({
                "status": "okay",
                "message": "user logged out"
            }), 200)

        else:
            return make_response(jsonify({
                "status": "okay",
                "message": "user must be logged in"
            }), 400)

    @users_bp.route("/users", methods=["GET"])
    @jwt_required
    def users_all():
        if not session.get('logged_in_admin'):
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "Admin User must be logged in"
            }), 401)
        users = user_model.get_all()
        if not users:
            return make_response(jsonify({
                "status": "not found",
                "message": "users you are looking for do not esxist"
            }), 404)
        else:
            return make_response(
                jsonify({
                    "status": "ok",
                    "users": users
                }), 200)

    @users_bp.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
    @jwt_required
    def specific_user(user_id):
        if request.method == 'PUT':
            checks = registration_checker(request)
            if checks:
                return make_response(jsonify({
                    "status":"not acceptable",
                    "message":checks
                    }), 406)

            data = request.get_json()
            name = data['name']
            email = data['email']
            usrnm = data['username']
            pswrd = data['password']
            
            user = user_model.get_user_by_email(email)
            if user:
                return make_response(jsonify({
                    "status": "not acceptable",
                    "message": "user already exists"
                    }), 406)

            else:
                user = user_model.update_user(user_id, name, usrnm, pswrd)
                users = user_model.get_all()
                return make_response(jsonify({
                    "status": "created",
                    "user": user,
                    "users": users
                    }), 201)
                            
            
        elif request.method == 'DELETE':
            user_email = get_jwt_identity()
            print(user_email)
            user = user_model.get_user_role_by_email(user_email)
            if not user:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "Admin User must be logged in"
                    }), 401)

            users = user_model.delete_user(user_id)
            if users:
                return make_response(
                    jsonify({
                        "status": "ok",
                        "users": users
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "users you are looking for do not esxist"
                    }), 404)

        else:
            user = user_model.get_user_by_id(user_id)
            if user:
                return make_response(
                    jsonify({
                        "status": "ok",
                        "users": user
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "users you are looking for do not esxist"
                    }), 404)
