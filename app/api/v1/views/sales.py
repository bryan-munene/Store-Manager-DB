from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from ..models.sales import SalesModel
from ..models.items import ItemsModel

sales_bp = Blueprint('sales', __name__, url_prefix='/api/v2')


sales_model = SalesModel()

class Sales(object):
    @sales_bp.route("/make_sale", methods=["POST"])
    @jwt_required
    def make_sale():
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)

        if not request.is_json:
            return make_response(
                jsonify({
                    "status": "wrong format",
                    "message": "request not json"
                }), 400)
    
        data = request.get_json()
        payment_mode = data['payment_mode']
        ordered_items = data['sale_items']
        auth = auth_user['user_id']

        if payment_mode == "":
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "Please fill all the required fields"
            }), 406)

    
        if not len(ordered_items) == 0:
            for ordered_item in ordered_items:
                item_id = ordered_item.get('item_id')
                quantity = ordered_item.get('quantity')

                
                if quantity == "":
                    return make_response(jsonify({
                        "status": "not acceptable",
                        "message": "Please fill all the required fields"
                    }), 406)

                if item_id == "":
                    return make_response(jsonify({
                        "status": "not acceptable",
                        "message": "Please fill all the required fields"
                    }), 406)

                if not quantity.isdigit():
                    return make_response(jsonify({
                        "status": "not acceptable",
                        "message": "Quantity is not valid"
                    }), 400)

                if not item_id.isdigit():
                    return make_response(jsonify({
                        "status": "not acceptable",
                        "message": "Item id is not valid"
                    }), 400)

                item_id = int(item_id)
                items_model = ItemsModel()
                item = items_model.get_by_id(item_id)
                if not item:
                    return make_response(jsonify({
                        "status": "not found", 
                        "message": "item with item_id " + str(item_id) + " not found"
                        }), 404)
                                                
                
                name = item['name']
                price = item['price']
                stock_level = item['quantity']
                        
                if not stock_level:
                    return make_response(jsonify({
                    "status": "not acceptable", 
                    "message": "Item not available"
                    }), 406)
            
                if int(stock_level) < int(quantity) :
                    return make_response(jsonify({
                            "status": "not acceptable", 
                            "message": " we've run out of stock"
                        }), 406)
                    
                else:
                    total = int(quantity) * int(price)
                    sales_model.add_sale_items_list(item_id, name, quantity, price, total, auth)
                    stock_level = int(stock_level) - int(quantity)
                    items_model.update_item_quantity(item_id, stock_level)
                        
                           
                        
                grand = 0
                items = 0
                sale_items = sales_model.sale_items_list()
                
                for sale_item in sale_items:
                    num = sale_item.get('quantity')
                    total = sale_item.get('total')
                    grand = grand + int(total)
                    items = items + int(num)

            sale = sales_model.add_sales(payment_mode, grand, items, auth)
            sale_id = sales_model.last_sale_id()
            list_sale_items = sales_model.sale_items_list()
            for sale_item in list_sale_items:
                item_id = sale_item.get('item_id')
                item_name = sale_item.get('item_name')
                quantity = sale_item.get('quantity')
                price = sale_item.get('price')
                total = sale_item.get('total')
                sales_model.add_sale_items(sale_id, item_id, item_name, quantity, price, total, auth)
            sales = sales_model.get_all_sales()

            return make_response(jsonify({
                "status": "created",
                "sales": sales,
                "sale_items": sale_items,
                "sale": sale
            }), 201)
        else:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "You must order atleast one item"
            }), 406)

    @sales_bp.route("/sales", methods=["GET"])
    @jwt_required
    def sales_all():
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)
    
        auth_user_role = auth_user['is_admin']
        if not auth_user_role:
            user_id = auth_user[0]
            sales = sales_model.get_sales_by_user_id(user_id)
            if not sales:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "You are not authorised to view this record!"
                    }), 401)
            return make_response(jsonify({
                "status": "ok",
                "sales": sales
                }), 200)
            
        sales = sales_model.get_all_sales()

        if not sales:
            return make_response(jsonify({
                "status": "not found",
                "message": "sales don't exist"
            }), 404)
        return make_response(jsonify({
            "status": "ok",
            "sales": sales
            }), 200)

    @sales_bp.route('/sales/<int:sale_id>', methods=['GET'])
    @jwt_required
    def specific_sale(sale_id):
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)
    
        auth_user_role = auth_user['is_admin']
        if auth_user_role:
            sale = sales_model.get_sales_by_sale_id(sale_id)

            if not sale:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "sale you are looking for does not exist"
                }), 404)

            else:
                return make_response(jsonify({
                    "status": "ok",
                    "sale": sale
                }), 200)
        else:
            user_id = auth_user['user_id']
            sale = sales_model.get_sales_by_sale_id(sale_id)
            creator = sale['created_by']
            if not sale:
                return make_response(jsonify({
                    "status": "not found",
                    "message": "sale not found"
                    }), 404)
            elif sale and user_id != creator:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "You are not authorised to view this sale"
                    }), 401)
            else:
                return make_response(jsonify({
                    "status": "ok",
                    "sale": sale
                    }), 200)
