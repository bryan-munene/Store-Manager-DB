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
       

def categories_checker(request):
    '''
    this function checks all the inputs for the categories part
    '''
    
    if not request.is_json:
        return "request not json"
    
    data = request.get_json()
    name = data['name']
    description = data['email']
     
    if name == "" or description =="":
        return "Please fill all the required fields"
    
    