from flask import Blueprint, request, jsonify, make_response, session
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity)
from ..models.sales import SalesModel, sale_items_temp
from ..models.items import ItemsModel
from ..utility.validators import system_error_sales, sales_checker

sales_bp = Blueprint('sales', __name__, url_prefix='/api/v2')


sales_model = SalesModel()


class Sales(object):
    '''Handles the application logic of the users part'''
    def __init__(self=None, *args, **kwargs):
        '''initializes the class and it's variables'''
        self.request = request

    @sales_bp.route("/make_sale", methods=["POST"])
    @jwt_required
    def make_sale(*args, **kwargs):
        '''handles the creation of a sale'''
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)

        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'True':
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "Admin User cannot make a sale"
            }), 401)

        sys_checks = system_error_sales(request)
        if sys_checks:
            return make_response(jsonify({
                "status": "server error",
                "message": "we encountered a system error try again"
            }), 500)
        checks = sales_checker(request)
        if checks:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": checks
            }), 406)

        data = request.get_json()
        payment_mode = data['payment_mode']
        ordered_items = data['sale_items']
        auth = auth_user['user_id']

        if payment_mode == "":
            return "Please fill all the required fields"

        if not len(ordered_items) == 0:
            for ordered_item in ordered_items:
                item_id = ordered_item.get('item_id')
                quantity = ordered_item.get('quantity')

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

                if int(stock_level) < int(quantity):
                    return make_response(jsonify({
                        "status": "not acceptable",
                        "message": " we've run out of stock"
                    }), 406)

                else:
                    total = int(quantity) * int(price)
                    sales_model.add_sale_items_list(
                        item_id, name, quantity, price, total, auth)
                    stock_level = int(stock_level) - int(quantity)
                    items_model.update_item_quantity(item_id, stock_level)

                grand = 0
                items = 0
                sale_items = sale_items_temp

                for sale_item in sale_items:
                    num = sale_item.get('quantity')
                    total = sale_item.get('total')
                    grand = grand + int(total)
                    items = items + int(num)

            sale = sales_model.add_sales(payment_mode, items, grand, auth)
            sale_id = sales_model.last_sale_id()
            list_sale_items = sale_items_temp
            for sale_item in list_sale_items:
                item_id = sale_item.get('item_id')
                item_name = sale_item.get('item_name')
                quantity = sale_item.get('quantity')
                price = sale_item.get('price')
                total = sale_item.get('total')
                sales_model.add_sale_items(
                    sale_id, item_id, item_name, quantity, price, total, auth)
            del sale_items_temp[:]
            sold_items = sales_model.get_sale_items_by_sale_id(sale_id)
            return make_response(jsonify({
                "status": "created",
                "sale_items": sold_items,
                "sale": sale
            }), 201)
        else:
            return make_response(jsonify({
                "status": "not acceptable",
                "message": "You must order atleast one item"
            }), 406)

    @sales_bp.route("/sales", methods=["GET"])
    @jwt_required
    def sales_all(*args, **kwargs):
        '''handles the retrieval of all sales'''
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)

        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'false':
            user_id = auth_user['user_id']
            sales = sales_model.get_sales_by_user_id(user_id)
            if not sales:
                return make_response(jsonify({
                    "status": "unauthorised",
                    "message": "You don't have any sales records!"
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
        '''handles the retrieval of a specific sale'''
        auth_user = get_jwt_identity()
        if not auth_user:
            return make_response(jsonify({
                "status": "unauthorised",
                "message": "User must be logged in"
            }), 401)

        auth_user_role = auth_user['is_admin']
        if auth_user_role == 'True':
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
