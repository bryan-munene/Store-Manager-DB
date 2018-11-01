import pytest
import unittest
from flask import json
from .setup_tests import Store_Manager_Base

store_manager = Store_Manager_Base()


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
class Test_Items(Store_Manager_Base):
    #GET ALL ITEMS TESTS


    def test_items_retrive_all_no_item(self):
        response= self.test_client.get('/api/v2/items',content_type='application/json')
        assert(response.status_code==404)


    def test_items_retrive_all_successfully(self):
        response= self.test_client.get('/api/v2/items',content_type='application/json')
        assert(response.status_code==200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #ADD ITEM TESTS


    def test_items_price_not_digit(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[0] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_price_not_digit1(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[1] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_item_name_not_str(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[2] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_item_name_empty(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[3] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_price_empty(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[4] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_image_empty(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[5] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_quantity_not_digit(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[6] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_quantity_not_digit1(self):
        response= self.test_client.post('/api/v2/add_item', data=sample_item[7] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_successfully(self):
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[8]) ,content_type='application/json')
        json.loads(response.data)
        assert(response.status_code==201)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #GET SPECIFIC ITEM TESTS

    #BY ID

    def test_get_item_negative_identifier(self):
        response= self.test_client.get('/api/v2/items/-1' ,content_type='application/json')
        assert(response.status_code == 404)

    def test_get_item_not_created(self):
        response= self.test_client.get('/api/v2/items/100' ,content_type='application/json')
        assert(response.status_code == 404)

    def test_get_item_successfully(self):
        response= self.test_client.get('/api/v2/items/1' ,content_type='application/json')
        assert(response.status_code == 200)


    #BY CATEGORY

    def test_get_items_by_category_not_created(self):
        response= self.test_client.get('/api/v2/items/painkillers' ,content_type='application/json')
        assert(response.status_code == 404)

    def test_get_items_successfully(self):
        response= self.test_client.get('/api/v2/items/antibiotics' ,content_type='application/json')
        assert(response.status_code == 200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #UPDATE ITEM TESTS

    #FIND ITEM TESTS

    def test_update_item_nonexistent(self):
        response= self.test_client.put('/api/v2/items/100', data=sample_item_updates[0] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_update_price_not_digit(self):
        response= self.test_client.put('/api/v2/items/1', data=sample_item_updates[1] ,content_type='application/json')
        assert(response.status_code==405)

    def test_items_update_price_not_digit1(self):
        response= self.test_client.put('/api/v2/items/1', data=sample_item_updates[2] ,content_type='application/json')
        assert(response.status_code==400)
        
    def test_items_update_item_name_not_str(self):
        response= self.test_client.put('/api/v2/add_item', data=sample_item_updates[3] ,content_type='application/json')
        assert(response.status_code==405)

    def test_items_update_item_name_empty(self):
        response= self.test_client.put('/api/v2/items/1', data=sample_item_updates[4] ,content_type='application/json')
        assert(response.status_code==400)

    def test_items_update_quantity_not_digit(self):
        response= self.test_client.put('/api/v2/items/1', data=sample_item_updates[5] ,content_type='application/json')
        assert(response.status_code==405)

    def test_items_update_quantity_not_digit1(self):
        response= self.test_client.put('/api/v2/items/1', data=sample_item_updates[6] ,content_type='application/json')
        assert(response.status_code==400)

    def test_update_item_empty(self):
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[7]) ,content_type='application/json')
        assert(response.status_code==403)

    def test_update_item_price_only_successfully(self):
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[8]) ,content_type='application/json')
        assert(response.status_code==200)

    def test_update_item_name_only_successfully(self):
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[9]) ,content_type='application/json')
        assert(response.status_code==200)

    def test_update_item_quantity_only_successfully(self):
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[10]) ,content_type='application/json')
        assert(response.status_code==200)

    def test_update_item_image_only_successfully(self):
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[11]) ,content_type='application/json')
        assert(response.status_code==200)

    def test_update_item_all_successfully(self):
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[12]) ,content_type='application/json')
        assert(response.status_code==200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #DELETE SPECIFIC ITEM TESTS


    def test_delete_item_negative_identifier(self):
        response= self.test_client.delete('/api/v2/items/-1' ,content_type='application/json')
        assert(response.status_code == 404)

    def test_delete_item_not_created(self):
        response= self.test_client.delete('/api/v2/items/100' ,content_type='application/json')
        assert(response.status_code == 404)

    def test_delete_item_successfully(self):
        response= self.test_client.delete('/api/v2/items/1' ,content_type='application/json')
        assert(response.status_code == 200)


    '''-------------------------------------------------------------------------------------------------------------------------------'''
