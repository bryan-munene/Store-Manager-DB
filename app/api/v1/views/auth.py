from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
import datetime
from app import blacklist

from ..models.auth import UserModel
from ..utility.validators import json_checker, login_checker, registration_checker, system_error_login, system_error_registration, update_checker, update_role_checker

users_bp = Blueprint('users', __name__, url_prefix='/api/v2')

user_model = UserModel()

class Users(object):
    @users_bp.route("/login", methods=["POST"])
    def user_login():
        user = get_jwt_identity()
        if user:
            return make_response(jsonify({
                "status":"Forbidden",
                "message":"You are already logged in"
                }), 403)

        sys_checks = system_error_login(request)
        if sys_checks:
            return make_response(jsonify({
                "status":"we encountered a system error try again",
                "message":sys_checks
                }), 500)
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
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
                }), 401)
    
        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'false':
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "Admin User must be logged in"
                }), 401)
        
        sys_checks = system_error_registration(request)
        if sys_checks:
            return make_response(jsonify({
                "status":"we encountered a system error try again",
                "message":sys_checks
                }), 500)
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

    @users_bp.route("/logout", methods=["DELETE"])
    @jwt_required
    def logout():
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return jsonify({"msg": "Successfully logged out"}), 200

    @users_bp.route("/users", methods=["GET"])
    @jwt_required
    def users_all():
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
                }), 401)
    
        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'false':
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
        return make_response(
            jsonify({
                "status": "ok",
                "users": users
                }), 200)

    @users_bp.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
    @jwt_required
    def specific_user(user_id):
        if request.method == 'PUT':
            auth_user = get_jwt_identity()
            if not auth_user:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "User must be logged in"
                    }), 401)
        
            auth_user_role = auth_user['is_admin']
            if auth_user_role == 'false':
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "Admin User must be logged in"
                    }), 401)
            
            checks = update_checker(request)
            if checks:
                return make_response(jsonify({
                    "status":"not acceptable",
                    "message":checks
                    }), 406)

            data = request.get_json()
            name = data['name']
            usrnm = data['username']
            pswrd = data['password']
            
            user = user_model.get_user_by_id(user_id)
            if not user:
                return make_response(jsonify({
                    "status": "not acceptable",
                    "message": "user does not exist"
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
            auth_user = get_jwt_identity()
            if not auth_user:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "User must be logged in"
                    }), 401)
        
            auth_user_role = auth_user['is_admin']
            if auth_user_role == 'false':
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "Admin User must be logged in"
                    }), 401) 

            users = user_model.delete_user(user_id)
            print(user_id)
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
            auth_user = get_jwt_identity()
            if not auth_user:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "User must be logged in"
                    }), 401)
        
            auth_user_role = auth_user['is_admin']
            if auth_user_role == 'false':
                id = user_model.get_user_id_by_email(auth_user['email'])
                if id != user_id:
                    return make_response(jsonify({
                        "status": "unauthorised",
                        "message": "You are not authorised to view this record!"
                        }), 401)
            
        
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


    @users_bp.route("/role/<int:user_id>", methods=["PUT"])
    @jwt_required
    def user_role(user_id):
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
                }), 401)
    
        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'false':
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "Admin User must be logged in"
                }), 401)
        
        checks = update_role_checker(request)
        if checks:
            return make_response(jsonify({
                "status":"not acceptable",
                "message":checks
                }), 406)

        data = request.get_json()
        role = data['is_admin']
        
        user = user_model.get_user_by_id(user_id)
        if not user:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "user does not exist"
                }), 406)

        else:
            user = user_model.update_user_role(user_id, role)
            users = user_model.get_all()
            return make_response(jsonify({
                "status": "created",
                "user": user,
                "users": users
                }), 201)
                        
        