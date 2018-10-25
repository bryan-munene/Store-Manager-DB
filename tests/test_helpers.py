from flask import json
import pytest


sample_user=[
            {
            "name":"test",
            "email":"testee@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "email":"test@mail.com",	
            "password":"pass"
            },
            {
            "email":"test@adminmail.com",	
            "password":"pass"
            }
]


sample_item = [
    {"name":"Panadol", "price":"200",	"image":"image", "quantity":"12"},
    {"name":"Amoxil", "price":"200",	"image":"image", "quantity":"12"}
]


sample_sale = [{
            "payment_mode":"Cash",
            "sale_items": [
    	                    {
    		                "item_id":"1",
    		                "quantity":"1"
    	                    },
    	                    {
    		                "item_id":"2",
    		                "quantity":"1"
    	                    }
                           ]
            }
]

def sign_up_helper(test_client):
    '''
    this is a helper function for an ordinary user's registration
    '''
    sign_in_admin_helper(test_client)
    sign_up = test_client.post('/api/v1/register', data = json.dumps(sample_user[0]), content_type = 'application/json')
    assert (sign_up.status_code == 201)
    logout= test_client.get('/api/v1/logout', content_type = 'application/json')
    assert(logout.status_code == 200)
    
def sign_in_helper(test_client):
    '''
    this is a helper function for an ordinary user's login
    '''
    sign_up_helper(test_client)
    sign_in = test_client.post('/api/v1/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
    assert (sign_in.status_code == 200)
    
def sign_in_helper_2(test_client):
    '''
    this is a helper function for an ordinary user's login
    '''
    sign_in = test_client.post('/api/v1/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
    assert (sign_in.status_code == 200)

def sign_in_admin_helper(test_client):
    '''
    this is a helper function for an admin user's login
    '''
    sign_in = test_client.post('/api/v1/login', data = json.dumps(sample_user[2]), content_type = 'application/json')
    assert (sign_in.status_code == 200)

def add_items_helper(test_client):
    '''
    this is a helper function for adding items
    '''
    add_item = test_client.post('/api/v1/add_item', data=json.dumps(sample_item[0]) ,content_type='application/json')
    assert(add_item.status_code==201)
    add_item = test_client.post('/api/v1/add_item', data=json.dumps(sample_item[1]) ,content_type='application/json')
    assert(add_item.status_code==201)
    
def make_sale_helper(test_client):
    '''
    this is a helper function to make a sale
    '''
    sell = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[0]) ,content_type='application/json')
    assert(sell.status_code==201)
    