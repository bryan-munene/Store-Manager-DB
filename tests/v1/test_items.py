import pytest
from flask import json
from tests.test_helpers import make_sale_helper, sign_in_admin_helper, sign_in_helper, add_items_helper
from .setup_tests import app, db



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


sample_category = [
    {"name":"painkillers", "description":""},
    {"name":"", "description":"alleviates pain"},
    {"name":"", "description":""},
    {"name":"18+", "description":"for sale to persons above 18 years"},
    {"name":"painkillers", "description":"alleviates pain"}
]


sample_category_update  = [
    {"name":"antibiotics", "description":""},
    {"name":"", "description":"cures bacterial diseases"},
    {"name":"", "description":""},
    {"name":"21+", "description":"for sale to persons above 21 years"},
    {"name":"antibiotics", "description":"cures bacterial diseases"}
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

#BY ID

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


#BY CATEGORY

def test_get_items_by_category_not_created():
    test_client=app.test_client()
    response= test_client.get('/api/v1/items/painkillers' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_items_successfully():
    test_client=app.test_client()
    response= test_client.get('/api/v1/items/antibiotics' ,content_type='application/json')
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


'''-------------------------------------------------------------------------------------------------------------------------------'''

#CATEGORIES

#CREATE CATEGORY

def test_items_category_description_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category[0] ,content_type='application/json')
    assert(response.status_code==201)

def test_items_category_name_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category[1] ,content_type='application/json')
    assert(response.status_code==406)

def test_items_category_both_name_and_description_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category[2] ,content_type='application/json')
    assert(response.status_code==406)

def test_items_category_name_not_str():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category[3] ,content_type='application/json')
    assert(response.status_code==201)

def test_items_category_both_name_and_description_filled():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category[4] ,content_type='application/json')
    assert(response.status_code==201)

def test_items_category_duplicate():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category[4] ,content_type='application/json')
    assert(response.status_code==403)


'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET SPECIFIC CATEGORY TESTS

#BY ID

def test_get_category_negative_identifier():
    test_client=app.test_client()
    response= test_client.get('/api/v1/categories/-1' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_category_not_created():
    test_client=app.test_client()
    response= test_client.get('/api/v1/categories/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_category_successfully():
    test_client=app.test_client()
    response= test_client.get('/api/v1/categories/1' ,content_type='application/json')
    assert(response.status_code == 200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET ALL CATEGORIES TESTS


def test_items_category_retrive_all_no_category():
    test_client=app.test_client()
    response= test_client.get('/api/v1/categories',content_type='application/json')
    assert(response.status_code==404)


def test_items_category_retrive_all_category_successfully():
    test_client=app.test_client()
    add_items_helper(test_client)
    response= test_client.get('/api/v1/categories',content_type='application/json')
    assert(response.status_code==200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#DELETE SPECIFIC CATEGORY TESTS

#BY ID

def test_delete_category_negative_identifier():
    test_client=app.test_client()
    response= test_client.delete('/api/v1/categories/-1' ,content_type='application/json')
    assert(response.status_code == 404)

def test_delete_category_not_created():
    test_client=app.test_client()
    response= test_client.delete('/api/v1/categories/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_delete_category_successfully():
    test_client=app.test_client()
    response= test_client.delete('/api/v1/categories/1' ,content_type='application/json')
    assert(response.status_code == 200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

#UPDATE CATEGORY

def test_items_update_category_description_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category_update[0] ,content_type='application/json')
    assert(response.status_code==200)

def test_items_update_category_name_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category_update[1] ,content_type='application/json')
    assert(response.status_code==406)

def test_items_update_category_both_name_and_description_empty():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category_update[2] ,content_type='application/json')
    assert(response.status_code==406)

def test_items_update_category_name_not_str():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category_update[3] ,content_type='application/json')
    assert(response.status_code==200)

def test_items_update_category_both_name_and_description_filled():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category_update[4] ,content_type='application/json')
    assert(response.status_code==200)

def test_items_update_category_duplicate():
    test_client=app.test_client()
    response= test_client.post('/api/v1/categories', data=sample_category_update[4] ,content_type='application/json')
    assert(response.status_code==403)


'''-------------------------------------------------------------------------------------------------------------------------------'''
