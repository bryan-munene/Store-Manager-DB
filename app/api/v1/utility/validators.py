from flask import make_response, jsonify, json
import re

def login_checker(request):
    '''
    this function checks the validity of all the inputs for the registration part
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
    
def json_checker(request):
    '''
    this function checks the validity of if the request object is in json form
    '''
    if not request.is_json:
        return False
    return True


def system_error_login(request):
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
    
    if name == "" or email =="" or usrnm == "" or pswrd == "" or pswrd2 == "":
        return "Please fill all the required fields"
    
    if not pswrd == pswrd2:
        return "passwords don't match"
     

    if not re.match(
        "^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$",
            email, re.IGNORECASE):
        return "Email Provided is not in email format"
       
def update_checker(request):
    '''
    this function checks all the inputs for the registration part
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
     
    if name == "" or description =="":
        return "Please fill all the required fields"
    
    
def items_checker(request):
    '''
    this function checks all the inputs for the items part
    '''
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


def system_error_items(request):
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
    this function checks all the inputs for the items part
    '''
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


def system_error_items_update(request):
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
    this function checks all the inputs for the update user role part
    '''
    
    if not request.is_json:
        return "request not json"
    
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

def system_error_update_stock(request):
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

        