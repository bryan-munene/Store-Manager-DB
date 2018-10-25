import pytest
from flask import json
from app import create_app
from app.api.v1.views.auth import Users
from tests.test_helpers import sign_in_admin_helper, sign_in_helper, sign_up_helper

testusers = Users()

config = "testing"
app = create_app(config)


#REGISTRATION INPUT FOR TESTS

sample_registration = [
            {
            "name":"",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":""
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"testmail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass1"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass11",
            "password2":"pass1"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            }
        ]


#LOGIN CREDENTIALS FOR TESTS

sample_login = [
            {
            "email":"",	
            "password":"pass"
            },
            {
            "email":"test@mail.com",	
            "password":""
            },
            {
            "email":"testmail.com",	
            "password":"pass"
            },
            {
            "email":"test@mail.com",	
            "password":"pass"
            },
            {
            "email":"teste@mail.com",	
            "password":"pass1"
            },
            {
            "email":"teste@mail.com",	
            "password":"pass1"
            },
            {
            "email":"test@adminmail.com",	
            "password":"pass"
            },
            {"email":"test@mail.com", 
            "password":"pass"
            }
        ]



'''-------------------------------------------------------------------------------------------------------------------------------'''

#LOGIN TESTS

#INPUT CHECKS

    
def test_login_empty_email():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = sample_login[0], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_empty_password():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = sample_login[1], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_wrong_email_format():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = sample_login[2], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_wrong_email_format2():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = sample_login[3], content_type = 'application/json')
    assert(response.status_code == 400)


#CREDENTIALS CHECK

def test_login_wrong_password():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = sample_login[4], content_type = 'application/json')
    assert(response.status_code == 400)

def test_login_wrong_email():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = sample_login[5], content_type = 'application/json')
    assert(response.status_code == 400)


#CORRECT CREDENTIALS

def test_login_correct_data():
    test_client = app.test_client()
    response = test_client.post('/api/v1/login', data = json.dumps(sample_login[6]), content_type = 'application/json')
    json.loads(response.data.decode('utf-8'))
    assert(response.status_code == 200)


'''-------------------------------------------------------------------------------------------------------------------------------'''

#REGISTRATION TESTS

def test_register_without_admin_logged_in():
    test_client = app.test_client()
    response = test_client.post('/api/v1/register', data = sample_registration[9], content_type = 'application/json')
    assert(response.status_code == 401)


#USER INPUT CHECKS
  
def test_register_empty_name():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[0], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_email():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[1], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_username():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[2], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_password():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[3], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_empty_password2():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[4], content_type = 'application/json')
    assert(response.status_code == 400)


#EMAIL FORMAT CHECKS

def test_register_wrong_email_format():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[5], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_wrong_email_format1():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[6], content_type = 'application/json')
    assert(response.status_code == 400)


#PASSWORD CHECK

def test_register_passwords_matching():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[7], content_type = 'application/json')
    assert(response.status_code == 400)

def test_register_passwords_matching1():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[8], content_type = 'application/json')
    assert(response.status_code == 400)


#CORRECT INPUT

def test_register_correct_data():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = json.dumps(sample_registration[9]), content_type = 'application/json')
    json.loads(response.data.decode('utf-8'))
    assert (response.status_code == 201)


#DUPLICATE INPUT

def test_register_duplicate_input():
    test_client = app.test_client()
    sign_in_admin_helper(test_client)
    response = test_client.post('/api/v1/register', data = sample_registration[9], content_type = 'application/json')
    assert (response.status_code == 400)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#LOGOUT TESTS

def test_logout_correctly():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    response= test_client.get('/api/v1/logout', content_type = 'application/json')
    assert(response.status_code == 200)

def test_logout_without_logged_in():
    test_client=app.test_client()
    response= test_client.get('/api/v1/logout', content_type = 'application/json')
    assert(response.status_code == 400)


'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET ALL USERS TEST


def test_users_retrive_all_no_admin_login():
    test_client=app.test_client()
    response= test_client.get('/api/v1/users',content_type='application/json')
    assert(response.status_code==401)


def test_users_retrive_all_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    response= test_client.get('/api/v1/users',content_type='application/json')
    assert(response.status_code==200)


'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET SPECIFIC USER TEST


def test_users_retrive_user_no_admin_login():
    test_client=app.test_client()
    response= test_client.get('/api/v1/users/1',content_type='application/json')
    assert(response.status_code==401)

def test_users_retrive_user_not_created():
    test_client=app.test_client()
    response= test_client.get('/api/v1/users/100',content_type='application/json')
    assert(response.status_code==404)

def test_users_retrive_user_negative_id():
    test_client=app.test_client()
    response= test_client.get('/api/v1/users/-1',content_type='application/json')
    assert(response.status_code==404)

def test_users_retrive_user_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    response= test_client.get('/api/v1/users/1',content_type='application/json')
    assert(response.status_code==200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#UPDATE SPECIFIC USER TEST


def test_users_update_user_no_admin_login():
    test_client=app.test_client()
    response= test_client.put('/api/v1/users/1',content_type='application/json')
    assert(response.status_code==401)

def test_users_update_user_not_created():
    test_client=app.test_client()
    response= test_client.put('/api/v1/users/100',content_type='application/json')
    assert(response.status_code==404)

def test_users_update_user_negative_id():
    test_client=app.test_client()
    response= test_client.put('/api/v1/users/-1',content_type='application/json')
    assert(response.status_code==404)

def test_users_update_user_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    response= test_client.put('/api/v1/users/1',content_type='application/json')
    assert(response.status_code==200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#DELETE SPECIFIC USER TEST


def test_users_delete_user_no_admin_login():
    test_client=app.test_client()
    response= test_client.delete('/api/v1/users/1',content_type='application/json')
    assert(response.status_code==401)

def test_users_delete_user_not_created():
    test_client=app.test_client()
    response= test_client.delete('/api/v1/users/100',content_type='application/json')
    assert(response.status_code==404)

def test_users_delete_user_negative_id():
    test_client=app.test_client()
    response= test_client.delete('/api/v1/users/-1',content_type='application/json')
    assert(response.status_code==404)

def test_users_delete_user_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    response= test_client.delete('/api/v1/users/1',content_type='application/json')
    assert(response.status_code==200)
