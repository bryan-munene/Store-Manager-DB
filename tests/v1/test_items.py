import pytest
import unittest
from flask import json
from .setup_tests import Store_Manager_Base

store_manager = Store_Manager_Base()


sample_item = [
    {
	"name":"Panadol", 
	"price":"abc",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Amoxil", 
	"price":"-200",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"123", 
	"price":"220",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"", 
	"price":"220",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Panadol", 
	"price":"",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Panadol", 
	"price":"220",	
	"image":"", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Panadol", 
	"price":"220",	
	"image":"image", 
	"quantity":"abc", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Panadol", 
	"price":"220",	
	"image":"image", 
	"quantity":"-12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Panadol", 
	"price":"220",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"10"
    },
    {
	"name":"Panadol", 
	"price":"220",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    }
]

sample_item_updates=[
    {"name":"Panadol", "price":"300",	"image":"image1", "quantity":"15", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol", "price":"-300",	"image":"image1", "quantity":"15", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol", "price":"abc",	"image":"image1", "quantity":"15", "reorder_point":"3", "category_id":"1"},
    {"name":"123", "price":"300",	"image":"image1", "quantity":"15", "reorder_point":"3", "category_id":"1"},
    {"name":"", "price":"300",	"image":"image1", "quantity":"15", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol", "price":"300",	"image":"image1", "quantity":"abc", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol", "price":"300",	"image":"image1", "quantity":"-15", "reorder_point":"3", "category_id":"1"},
    {"name":"", "price":"",	"image":"", "quantity":"","reorder_point":"", "category_id":""},
    {"name":"Panadol", "price":"300",	"image":"image", "quantity":"12", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol Advance", "price":"200",	"image":"image", "quantity":"12", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol", "price":"200",	"image":"image", "quantity":"15", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol", "price":"200",	"image":"image1", "quantity":"12", "reorder_point":"3", "category_id":"1"},
    {"name":"Panadol Advance", "price":"300",	"image":"image1", "quantity":"15", "reorder_point":"3", "category_id":"1"}
]


'''-------------------------------------------------------------------------------------------------------------------------------'''
class Test_Items(Store_Manager_Base):
    #GET ALL ITEMS TESTS


    def test_items_retrive_all_no_item(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/items',content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code==404)


    def test_items_retrive_all_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.get('/api/v2/items',content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code==200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #ADD ITEM TESTS


    def test_items_price_not_digit(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_price_not_digit1(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_item_name_not_str(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_item_name_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_price_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[4]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_image_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[5]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_quantity_not_digit(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[6]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_quantity_not_digit1(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[7]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_no_category(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[8]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_category_helper()
        response= self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[9]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #GET SPECIFIC ITEM TESTS

    #BY ID

    def test_get_item_negative_identifier(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/items/-1' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code == 404)

    def test_get_item_not_created(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/items/100' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code == 404)

    def test_get_item_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.get('/api/v2/items/1' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code == 200)


    
    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #UPDATE ITEM TESTS

    #FIND ITEM TESTS

    def test_update_item_nonexistent(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.put('/api/v2/items/100', data=json.dumps(sample_item_updates[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code==404)

    def test_items_update_price_not_digit(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_price_not_digit1(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)
        
    def test_items_update_item_name_not_str(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/add_item', data=json.dumps(sample_item_updates[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_item_name_empty(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[4]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_quantity_not_digit(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[5]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_quantity_not_digit1(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[6]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_update_item_empty(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[7]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "forbidden")
        assert(response.status_code==403)

    def test_update_item_price_only_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[8]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_update_item_name_only_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[9]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_update_item_quantity_only_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[10]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_update_item_image_only_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[11]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_update_item_all_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.put('/api/v2/items/1', data=json.dumps(sample_item_updates[12]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #DELETE SPECIFIC ITEM TESTS


    def test_delete_item_negative_identifier(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.delete('/api/v2/items/-1' ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(response.status_code == 404)

    def test_delete_item_not_created(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.delete('/api/v2/items/100' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code == 404)

    def test_delete_item_successfully(self):
        self.token = store_manager.sign_in_admin()
        store_manager.add_items_helper()
        response= self.test_client.delete('/api/v2/items/1' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code == 200)


    '''-------------------------------------------------------------------------------------------------------------------------------'''
