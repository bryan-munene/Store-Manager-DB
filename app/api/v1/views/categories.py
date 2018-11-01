from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from ..models.categories import CategoriesModel
from ..utility.validators import categories_checker

categories_model = CategoriesModel()

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v2')


class Categories(object):
    def __init__(self=None, *args, **kwargs):
        self.request = request
        
    @categories_bp.route('/add_category', methods=["POST"])
    @jwt_required
    def add_categories(*args, **kwargs):
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

        checks = categories_checker(request)
        if checks:
            return make_response(jsonify({
                "status":"not acceptable",
                "message":checks
                }), 406)

        data = request.get_json()
        name = data['name']
        description = data['description']
        auth = auth_user['user_id']
        name = name.lower()
        
        category = categories_model.get_by_name(name)
        if category:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "category already exists"
                }), 406)
        else:
            category = categories_model.add_category(name, description, auth)
            categories = categories_model.get_all()
            return make_response(jsonify({
                "status": "created",
                "category": category,
                "categories": categories
                }), 201)
    
    @categories_bp.route('/categories', methods=["GET"])
    @jwt_required
    def get_all_categories(*args, **kwargs):
        categories = categories_model.get_all()
        if not categories:
            return make_response(jsonify({
                "status": "not found",
                "message": "categories do not exists"
                }), 404)

        else:
            return make_response(jsonify({
                "status": "ok",
                "categories": categories
                }), 200)

    @categories_bp.route("/categories/<int:category_id>", methods=["GET", "PUT", "DELETE"])
    @jwt_required
    def specific_user(category_id):
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
            
            checks = categories_checker(request)
            if checks:
                return make_response(jsonify({
                    "status":"not acceptable",
                    "message":checks
                    }), 406)

            data = request.get_json()
            name = data['name']
            description = data['description']
            
            category = categories_model.get_by_id(category_id)
            if not category:
                return make_response(jsonify({
                    "status": "not acceptable",
                    "message": "category does not exist"
                    }), 406)

            else:
                category = categories_model.update_category(category_id, name, description)
                categories = categories_model.get_all()
                return make_response(jsonify({
                    "status": "created",
                    "category": category,
                    "categories": categories
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

            categories = categories_model.delete_category(category_id)
            if categories:
                return make_response(
                    jsonify({
                        "status": "ok",
                        "categories": categories
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "users you are looking for do not esxist"
                    }), 404)

        else:
            category = categories_model.get_by_id(category_id)
            if category:
                return make_response(
                    jsonify({
                        "status": "ok",
                        "category": category
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "category you are looking for do not esxist"
                    }), 404)
