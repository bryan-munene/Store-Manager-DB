from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity)
from ..models.items import ItemsModel
from ..models.categories import CategoriesModel
from ..utility.validators import system_error_items, items_checker, system_error_items_update, items_update_checker, update_stock_checker, system_error_update_stock

items_model = ItemsModel()
categories_model = CategoriesModel()

items_bp = Blueprint('items', __name__, url_prefix='/api/v2')

@items_bp.route("/")
def index():
    return jsonify(200, "WELCOME. You are here.")


class Items(object):
    '''Handles the application logic of the items part'''
    def __init__(self=None, *args, **kwargs):
        '''initializes the class and it's variables'''
        self.request = request

    @items_bp.route('/add_item', methods=["POST"])
    @jwt_required
    def add_items(*args, **kwargs):
        '''handles the creation of new items'''
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

        sys_checks = system_error_items(request)
        if sys_checks:
            return make_response(jsonify({
                "status": "server error",
                "message": "we encountered a system error try again"
            }), 500)
        checks = items_checker(request)
        if checks:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": checks
            }), 406)

        data = request.get_json()
        name = data['name']
        price = data['price']
        image = data['image']
        quantity = data['quantity']
        reorder_point = data['reorder_point']
        category_id = data['category_id']
        auth = auth_user['user_id']
        name = name.lower()

        category = categories_model.get_by_id(category_id)
        if not category:
            return make_response(jsonify({
                "status": "not found",
                "message": "category does not esxist"
            }), 404)

        item = items_model.get_by_name_and_price(name, price)
        if item:
            return make_response(
                jsonify({
                    "status": "forbidden",
                    "message": "item already exists"
                }), 403)

        item = items_model.add_item(
            name,
            price,
            quantity,
            image,
            category_id,
            reorder_point,
            auth)
        return make_response(
            jsonify({
                "status": "created",
                "item": item
            }), 201)

    @items_bp.route("/items", methods=["GET"])
    @jwt_required
    def items_all(*args, **kwargs):
        '''handle the display of all items'''
        items = items_model.get_all()
        if not items:
            return make_response(jsonify({
                "status": "not found",
                "message": "items you are looking for does not esxist"
            }), 404)
        else:
            return make_response(
                jsonify({
                    "status": "ok",
                    "items": items
                }), 200)

    @items_bp.route('/items/<int:item_id>', methods=["GET", "PUT", "DELETE"])
    @jwt_required
    def specific_item(item_id):
        '''handles the update, deletion and retrieval of a specific item'''
        if request.method == 'PUT':
            '''handles the update'''
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

            sys_checks = system_error_items_update(request)
            if sys_checks:
                return make_response(jsonify({
                    "status": "server error",
                    "message": "we encountered a system error try again"
                }), 500)
            checks = items_update_checker(request)
            if checks:
                return make_response(jsonify({
                    "status": "not acceptable",
                    "message": checks
                }), 406)

            data = request.get_json()
            price = data['price']
            image = data['image']
            quantity = data['quantity']
            reorder_point = data['reorder_point']
            category_id = data['category_id']
            auth = auth_user['user_id']

            category = categories_model.get_by_id(category_id)
            if not category:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "category does not esxist"
                }), 404)

            item = items_model.get_by_id(item_id)
            if not item:
                return make_response(
                    jsonify({
                        "status": "not found",
                        "message": "item does not exist"
                    }), 404)

            else:
                item = items_model.update_item(
                    item_id, price, quantity, image, category_id, reorder_point, auth)
                return make_response(jsonify({
                    "status": "created",
                    "item": item
                }), 201)

        elif request.method == 'DELETE':
            '''handles the deletion'''
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

            items = items_model.delete_item(item_id)
            if items:
                return make_response(
                    jsonify({
                        "status": "ok",
                        "items": items
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "Items you are looking for do not esxist"
                }), 404)

        else:
            '''handles the retrieval'''
            item = items_model.get_by_id(item_id)
            if item:
                return make_response(
                    jsonify({
                        "status": "ok",
                        "item": item
                    }), 200)
            else:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "Item you are looking for does not esxist"
                }), 404)

    @items_bp.route('/stock/<int:item_id>', methods=["PUT"])
    @jwt_required
    def item__stock(item_id):
        '''handles the update of the sock of a specific item'''
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

        sys_checks = system_error_update_stock(request)
        if sys_checks:
            return make_response(jsonify({
                "status": "server error",
                "message": "we encountered a system error try again"
            }), 500)
        checks = update_stock_checker(request)
        if checks:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": checks
            }), 406)

        data = request.get_json()
        quantity = data['quantity']

        item = items_model.get_by_id(item_id)
        if not item:
            return make_response(
                jsonify({
                    "status": "forbidden",
                    "message": "item does not exist"
                }), 403)

        else:
            stock = item['quantity']
            new_stock = int(stock) + int(quantity)
            item = items_model.update_item_quantity(item_id, new_stock)
            return make_response(jsonify({
                "status": "Updated",
                "item": item
            }), 201)
