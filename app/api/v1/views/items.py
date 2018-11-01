from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from ..models.items import ItemsModel
from ..models.categories import CategoriesModel

items_model = ItemsModel()
categories_model = CategoriesModel()

items_bp = Blueprint('items', __name__, url_prefix='/api/v2')



@items_bp.route("/")
def index():
    return jsonify(200, "WELCOME. You are here.")


class Items(object):
    def __init__(self=None, *args, **kwargs):
        self.request = request
        
    @items_bp.route('/add_item', methods=["POST"])
    @jwt_required
    def add_items(*args, **kwargs):
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

        if not request.is_json:
            return make_response(
                jsonify({
                    "status": "wrong format",
                    "messenge": "request not json"
                }), 400)
    
        data = request.get_json()
        name = data['name']
        price = data['price']
        image = data['image']
        quantity = data['quantity']
        reorder_point = data['reorder_point']
        category_id = data['category_id']
        auth = auth_user['user_id']
        name =name.lower()
        
        if name == "" or price == "" or image == "" or quantity == "":
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "all fields must be filled"
            }), 406)

        if not price.isdigit():
            return make_response(
                jsonify({
                    "status": "not acceptable",
                    "message": "price not valid"
                }), 400)

        if not name.isalpha():
            return make_response(
                jsonify({
                    "status": "not acceptable",
                    "message": "item name not valid"
                }), 400)

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

        item = items_model.add_item(name, price, quantity, category_id, reorder_point, auth)
        items = items_model.get_all()
        return make_response(
            jsonify({
                "status": "created",
                "item": item,
                "items": items
            }), 201)

    @items_bp.route("/items", methods=["GET"])
    @jwt_required
    def items_all(*args, **kwargs):
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
            
            if not request.is_json:
                return make_response(
                    jsonify({
                        "status": "wrong format",
                        "messenge": "request not json"
                    }), 400)
    
            data = request.get_json()
            price = data['price']
            image = data['image']
            quantity = data['quantity']
            reorder_point = data['reorder_point']
            category_id = data['category_id']
            auth = auth_user['user_id']
            
            if price == "" or image == "" or quantity == "":
                return make_response(jsonify({
                    "status": "not acceptable",
                    "message": "all fields must be filled"
                }), 406)

            if not price.isdigit():
                return make_response(
                    jsonify({
                        "status": "not acceptable",
                        "message": "price not valid"
                        }), 400)

            
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
                        "status": "forbidden",
                        "message": "item does not exist"
                        }), 403)

            else:
                item = items_model.update_item(item_id, price, quantity, category_id, reorder_point, auth)
                items = items_model.get_all()
                return make_response(jsonify({
                    "status": "created",
                    "item": item,
                    "items": items
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
        
        if not request.is_json:
            return make_response(
                jsonify({
                    "status": "wrong format",
                    "messenge": "request not json"
                }), 400)

        data = request.get_json()
        quantity = data['quantity']
                
        if quantity == "":
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "all fields must be filled"
            }), 406)

        if not quantity.isdigit():
            return make_response(
                jsonify({
                    "status": "not acceptable",
                    "message": "quantity not valid"
                    }), 400)

        
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
            items = items_model.get_all()
            return make_response(jsonify({
                "status": "Updated",
                "item": item,
                "items": items
                }), 201)
