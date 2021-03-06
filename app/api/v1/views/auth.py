from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt)
import datetime

from ..models.auth import UserModel, BlacklistModel
from app.api.v1.models.sales import SalesModel
from ..utility.validators import login_checker, registration_checker, system_error_login, system_error_registration, update_checker, update_role_checker, system_error_update, system_error_update_role

users_bp = Blueprint('users', __name__, url_prefix='/api/v2')

user_model = UserModel()
sales_model = SalesModel()
blacklist_model = BlacklistModel()

class Users(object):
    '''Handles the application logic of the users part'''
    def __init__(self=None, *args, **kwargs):
        '''initializes the class and it's variables'''
        self.request = request

    @users_bp.route("/login", methods=["POST"])
    def user_login(*args, **kwargs):
        '''handles login of users'''
        user = get_jwt_identity()
        if user:
            return make_response(jsonify({
                "status": "Forbidden",
                "message": "You are already logged in"
            }), 403)

        sys_checks = system_error_login(request)
        if sys_checks:
            return make_response(jsonify({
                "status": "Server error",
                "message": "we encountered a system error try again"
            }), 500)
        checks = login_checker(request)
        if checks:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": checks
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
        role = user_model.get_user_role_by_email(email)
        
        if credentials:
            return make_response(jsonify({
                "status": "user logged in",
                "username": username,
                "login": True,
                "role": role,
                "token": credentials
            }), 200)
        return make_response(jsonify({
            "status": "login error",
            "message": "Credentials do not match",
            "login": False
        }), 401)

    @users_bp.route("/dashboard", methods=["GET"])
    @jwt_required
    def dashboard(*args, **kwargs):
        '''handles the dashboard of all users and is a protected route'''
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)

        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'false':
            user_id = auth_user['user_id']
            last = sales_model.get_sales_by_user_id_last_five(user_id)
            count = sales_model.count_sales_by_user_id(user_id)
            return make_response(jsonify({
                "status": "Logged in",
                "count": count,
                "sales": last
                }), 200)

        last = sales_model.get_sales_last_five()
        count = sales_model.count_sales()
        return make_response(jsonify({
            "status": "Logged in admin",
            "count": count,
            "sales": last
            }), 200)
        

    @users_bp.route("/register", methods=["POST"])
    @jwt_required
    def register(*args, **kwargs):
        '''handles the registration of new users and is a protected route'''
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
                "status": "server error",
                "message": "we encountered a system error try again"
            }), 500)
        checks = registration_checker(request)
        if checks:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": checks
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
            return make_response(jsonify({
                "status": "created",
                "user": user
            }), 201)


    @users_bp.route("/logout", methods=["DELETE"])
    @jwt_required
    def logout(*args, **kwargs):
        '''handles user logout. it is a protected route'''
        jti = get_raw_jwt()['jti']
        blacklist_model.blacklist_token(jti)
        return make_response(jsonify({
            "status": "logged out",
            "message": "User successfully logged out"
        }), 200)

    @users_bp.route("/users", methods=["GET"])
    @jwt_required
    def users_all(*args, **kwargs):
        '''handles retrieval and display of all users'''
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
    def specific_user(user_id, *args, **kwargs):
        '''handles update, retrieval and deletion of a specific user'''
        if request.method == 'PUT':
            '''this handles the update part'''
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

            sys_checks = system_error_update(request)
            if sys_checks:
                return make_response(jsonify({
                    "status": "server error",
                    "message": "we encountered a system error try again"
                }), 500)
            checks = update_checker(request)
            if checks:
                return make_response(jsonify({
                    "status": "not acceptable",
                    "message": checks
                }), 406)

            data = request.get_json()
            name = data['name']
            usrnm = data['username']
            pswrd = data['password']

            user = user_model.get_user_by_id(user_id)
            if not user:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "user does not exist"
                }), 404)

            else:
                user = user_model.update_user(user_id, name, usrnm, pswrd)
                return make_response(jsonify({
                    "status": "created",
                    "user": user
                }), 201)

        elif request.method == 'DELETE':
            '''this handles the deletion of a specific user'''
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
            '''this is the retrieval of the specific user'''
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
                        "user": user
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "users you are looking for do not esxist"
                }), 404)

    @users_bp.route("/role/<int:user_id>", methods=["PUT"])
    @jwt_required
    def user_role(user_id):
        '''handles the update of a user's role to admin'''
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

        sys_checks = system_error_update_role(request)
        if sys_checks:
            return make_response(jsonify({
                "status": "server error",
                "message": "we encountered a system error try again"
            }), 500)
        checks = update_role_checker(request)
        if checks:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": checks
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
            return make_response(jsonify({
                "status": "created",
                "user": user
            }), 201)
