from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from ..models.categories import CategoriesModel
from ..utility.validators import categories_checker

categories_model = CategoriesModel()

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v2')


class Categories(object):
    @categories_bp.route('/add_item', methods=["POST"])
    @jwt_required
    def add_categories():
        checks = categories_checker(request)
        if checks:
            return make_response(jsonify({
                "status":"not acceptable",
                "message":checks
                }), 406)

        data = request.get_json()
        name = data['name']
        description = data['email']
        
        category = categories_model.get_by_name(name)
        if category:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "category already exists"
                }), 406)
        else:
            category = categories_model.add_category(name, description)
            categories = categories_model.get_all()
            return make_response(jsonify({
                "status": "created",
                "category": category,
                "categories": categories
                }), 201)
    
    @categories_bp.route('/add_item', methods=["POST"])
    @jwt_required
    def add_categories():
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