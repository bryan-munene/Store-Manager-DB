from flask import make_response, jsonify, json
import re


def login_checker(request):
    '''
    this function checks the validity of all the inputs for the login part
    '''
    if not request.is_json:
        return "request not json"

    data = request.get_json()
    email = data['email']
    password = data['password']

    if email == "":
        return "Please enter an email"

    elif password == "":
        return "Please enter a password"

    elif not re.match(
        "^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
            email, re.IGNORECASE):
        return "Email Provided is not in email format"

    else:
        return False



def system_error_login(request):
    '''
    this function checks all the keys for the input in login part
    '''
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def system_error_registration(request):
    '''
    this function checks all the keys for the input in registration part
    '''
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        usrnm = data['username']
        pswrd = data['password']
        pswrd2 = data['password2']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def system_error_update(request):
    '''
    this function checks all the keys for the input in user update part
    '''
    try:
        data = request.get_json()
        name = data['name']
        usrnm = data['username']
        pswrd = data['password']
        pswrd2 = data['password2']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def system_error_update_role(request):
    '''
    this function checks all the keys for the input in user update role part
    '''
    try:
        data = request.get_json()
        role = data['is_admin']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def registration_checker(request):
    '''
    this function checks all the inputs for the registration part
    '''

    if not request.is_json:
        return "request not json"

    data = request.get_json()
    name = data['name']
    email = data['email']
    usrnm = data['username']
    pswrd = data['password']
    pswrd2 = data['password2']

    if name == "" or email == "" or usrnm == "" or pswrd == "" or pswrd2 == "":
        return "Please fill all the required fields"

    if not pswrd == pswrd2:
        return "passwords don't match"

    if not re.match(
        "^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
            email, re.IGNORECASE):
        return "Email Provided is not in email format"


def update_checker(request):
    '''
    this function checks all the inputs for the update user part
    '''
    if not request.is_json:
        return "request not json"

    data = request.get_json()
    name = data['name']
    usrnm = data['username']
    pswrd = data['password']
    pswrd2 = data['password2']

    if name == "" or usrnm == "" or pswrd == "" or pswrd2 == "":
        return "Please fill all the required fields"

    if not pswrd == pswrd2:
        return "passwords don't match"


def update_role_checker(request):
    '''
    this function checks all the inputs for the update user role part
    '''

    if not request.is_json:
        return "request not json"

    data = request.get_json()
    role = data['is_admin']

    if role == "":
        return "Please fill all the required fields"


def categories_checker(request):
    '''
    this function checks all the inputs for the categories part
    '''

    if not request.is_json:
        return "request not json"

    data = request.get_json()
    name = data['name']
    description = data['description']

    if name == "" or description == "":
        return "Please fill all the required fields"


def items_checker(request):
    '''
    this function checks all the inputs for the items part
    '''
    if not request.is_json:
        return "request not json"

    data = request.get_json()
    name = data['name']
    price = data['price']
    image = data['image']
    quantity = data['quantity']

    if name == "" or price == "" or image == "" or quantity == "":
        return "all fields must be filled"

    if not price.isdigit():
        return "price not valid"

    if not name.isalpha():
        return "item name not valid"


def system_error_items(request):
    '''
    this function checks all the keys for the input in add item part
    '''
    try:
        data = request.get_json()
        name = data['name']
        price = data['price']
        image = data['image']
        quantity = data['quantity']
        reorder_point = data['reorder_point']
        category_id = data['category_id']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def items_update_checker(request):
    '''
    this function checks all the keys for the input in item update part
    '''
    if not request.is_json:
        return "request not json"

    data = request.get_json()
    price = data['price']
    image = data['image']
    quantity = data['quantity']

    if price == "" or image == "" or quantity == "":
        return "all fields must be filled"

    if not price.isdigit():
        return "price not valid"


def system_error_items_update(request):
    '''
    this function checks all the inputs for the update user role part
    '''
    try:
        data = request.get_json()
        price = data['price']
        image = data['image']
        quantity = data['quantity']
        reorder_point = data['reorder_point']
        category_id = data['category_id']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def update_stock_checker(request):
    '''
    this function checks all the inputs for the update item stock part
    '''
    if not request.is_json:
        return "request not json"

    data = request.get_json()
    quantity = data['quantity']

    if quantity == "":
        return "all fields must be filled"

    if not quantity.isdigit():
        return "quantity not valid"


def system_error_update_stock(request):
    '''
    this function checks all the keys for the input in item update stock part
    '''
    try:
        data = request.get_json()
        quantity = data['quantity']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def system_error_categories(request):
    '''
    this function checks all the keys for the input in categories section
    '''
    try:
        data = request.get_json()
        name = data['name']
        description = data['description']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e


def sales_checker(request):
    '''
    this function checks all the inputs for the sales part
    '''
    if not request.is_json:
        return "request not json"

    data = request.get_json()
    payment_mode = data['payment_mode']
    ordered_items = data['sale_items']

    if payment_mode == "":
        return "Please fill all the required fields"

    if not len(ordered_items) == 0:
        for ordered_item in ordered_items:
            item_id = ordered_item.get('item_id')
            quantity = ordered_item.get('quantity')

            if quantity == "":
                return "Please fill all the required fields"

            if item_id == "":
                return "Please fill all the required fields"

            if not quantity.isdigit():
                return "Quantity is not valid"

            if not item_id.isdigit():
                return "Item id is not valid"


def system_error_sales(request):
    '''
    this function checks all the keys for the input in sales part
    '''
    try:
        data = request.get_json()
        payment_mode = data['payment_mode']
        ordered_items = data['sale_items']
    except TypeError as e:
        return e
    except KeyError as e:
        return e
    except NameError as e:
        return e
    for ordered_item in ordered_items:
        try:
            item_id = ordered_item['item_id']
            quantity = ordered_item['quantity']
        except TypeError as e:
            return e
        except KeyError as e:
            return e
        except NameError as e:
            return e
