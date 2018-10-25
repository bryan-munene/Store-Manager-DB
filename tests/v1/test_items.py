import pytest
from flask import json
from app import create_app
from app.api.v1.views.items import Items
from app.api.v1.views.auth import Users
from tests.test_helpers import make_sale_helper, sign_in_admin_helper, sign_in_helper, add_items_helper

testitems = Items()
testusers = Users()

config = "testing"
app = create_app(config)


sample_item=[
    {"name":"Panadol", "price":"abc",	"image":"image", "quantity":"12"},
    {"name":"Panadol", "price":"-200",	"image":"image", "quantity":"12"},
    {"name":"123", "price":"200",	"image":"image", "quantity":"12"},
    {"name":"", "price":"200",	"image":"image", "quantity":"12"},
    {"name":"Panadol", "price":"",	"image":"image", "quantity":"12"},
    {"name":"Panadol", "price":"200",	"image":"", "quantity":"12"},
    {"name":"Panadol", "price":"200",	"image":"image", "quantity":"abc"},
    {"name":"Panadol", "price":"200",	"image":"image", "quantity":"-12"},
    {"name":"Panadol", "price":"250",	"image":"image", "quantity":"12"}
]


sample_item_updates=[
    {"name":"Panadol", "price":"300",	"image":"image1", "quantity":"15"},
    {"name":"Panadol", "price":"-300",	"image":"image1", "quantity":"15"},
    {"name":"Panadol", "price":"abc",	"image":"image1", "quantity":"15"},
    {"name":"123", "price":"300",	"image":"image1", "quantity":"15"},
    {"name":"", "price":"300",	"image":"image1", "quantity":"15"},
    {"name":"Panadol", "price":"300",	"image":"image1", "quantity":"abc"},
    {"name":"Panadol", "price":"300",	"image":"image1", "quantity":"-15"},
    {"name":"", "price":"",	"image":"", "quantity":""},
    {"name":"Panadol", "price":"300",	"image":"image", "quantity":"12"},
    {"name":"Panadol Advance", "price":"200",	"image":"image", "quantity":"12"},
    {"name":"Panadol", "price":"200",	"image":"image", "quantity":"15"},
    {"name":"Panadol", "price":"200",	"image":"image1", "quantity":"12"},
    {"name":"Panadol Advance", "price":"300",	"image":"image1", "quantity":"15"}
]




'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET ALL ITEMS TESTS


def test_items_retrive_all_no_item():
    test_client=app.test_client()
    response= test_client.get('/api/v1/items',content_type='application/json')
    assert(response.status_code==404)


def test_items_retrive_all_successfully():
    test_client=app.test_client()
    add_items_helper(test_client)
    response= test_client.get('/api/v1/items',content_type='application/json')
    assert(response.status_code==200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#ADD ITEM TESTS


def test_items_price_not_digit():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[0] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_price_not_digit1():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[1] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_item_name_not_str():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[2] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_item_name_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[3] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_price_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[4] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_image_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[5] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_quantity_not_digit():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[6] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_quantity_not_digit1():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=sample_item[7] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_successfully():
    test_client=app.test_client()
    response= test_client.post('/api/v1/add_item', data=json.dumps(sample_item[8]) ,content_type='application/json')
    json.loads(response.data)
    assert(response.status_code==201)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET SPECIFIC ITEM TESTS


def test_get_item_negative_identifier():
    test_client=app.test_client()
    response= test_client.get('/api/v1/items/-1' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_item_not_created():
    test_client=app.test_client()
    response= test_client.get('/api/v1/items/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_item_successfully():
    test_client=app.test_client()
    response= test_client.get('/api/v1/items/1' ,content_type='application/json')
    assert(response.status_code == 200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#UPDATE ITEM TESTS

#FIND ITEM TESTS

def test_update_item_nonexistent():
    test_client=app.test_client()
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/100', data=sample_item_updates[0] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_update_price_not_digit():
    test_client=app.test_client()
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=sample_item_updates[1] ,content_type='application/json')
    assert(response.status_code==405)

def test_items_update_price_not_digit1():
    test_client=app.test_client()
    response= test_client.put('/api/v1/items/1', data=sample_item_updates[2] ,content_type='application/json')
    assert(response.status_code==400)
    
def test_items_update_item_name_not_str():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/add_item', data=sample_item_updates[3] ,content_type='application/json')
    assert(response.status_code==405)

def test_items_update_item_name_empty():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=sample_item_updates[4] ,content_type='application/json')
    assert(response.status_code==400)

def test_items_update_quantity_not_digit():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=sample_item_updates[5] ,content_type='application/json')
    assert(response.status_code==405)

def test_items_update_quantity_not_digit1():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=sample_item_updates[6] ,content_type='application/json')
    assert(response.status_code==400)

def test_update_item_empty():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=json.dumps(sample_item_updates[7]) ,content_type='application/json')
    assert(response.status_code==403)

def test_update_item_price_only_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=json.dumps(sample_item_updates[8]) ,content_type='application/json')
    assert(response.status_code==200)

def test_update_item_name_only_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=json.dumps(sample_item_updates[9]) ,content_type='application/json')
    assert(response.status_code==200)

def test_update_item_quantity_only_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=json.dumps(sample_item_updates[10]) ,content_type='application/json')
    assert(response.status_code==200)

def test_update_item_image_only_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=json.dumps(sample_item_updates[11]) ,content_type='application/json')
    assert(response.status_code==200)

def test_update_item_all_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.put('/api/v1/items/1', data=json.dumps(sample_item_updates[12]) ,content_type='application/json')
    assert(response.status_code==200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#DELETE SPECIFIC ITEM TESTS


def test_delete_item_negative_identifier():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.delete('/api/v1/items/-1' ,content_type='application/json')
    assert(response.status_code == 404)

def test_delete_item_not_created():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.delete('/api/v1/items/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_delete_item_successfully():
    test_client=app.test_client()
    sign_in_admin_helper(test_client)
    add_items_helper(test_client)
    response= test_client.delete('/api/v1/items/1' ,content_type='application/json')
    assert(response.status_code == 200)