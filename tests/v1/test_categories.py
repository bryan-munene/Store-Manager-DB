import pytest
import unittest
from flask import json
from .setup_tests import Store_Manager_Base

store_manager = Store_Manager_Base()



sample_category = [
    {"name":"painkillers", "description":""},
    {"name":"", "description":"alleviates pain"},
    {"name":"", "description":""},
    {"name":"18+", "description":"for sale to persons above 18 years"},
    {"name":"painkillers2", "description":"alleviates pain"}
]


sample_category_update  = [
    {"name":"antibiotics", "description":""},
    {"name":"", "description":"cures bacterial diseases"},
    {"name":"", "description":""},
    {"name":"21+", "description":"for sale to persons above 21 years"},
    {"name":"antibiotics", "description":"cures bacterial diseases"}
]


class Test_Categories(Store_Manager_Base):
    
    #CATEGORIES
    
    #GET ALL CATEGORIES TESTS

    def test_items_category_retrive_all_category_successfully(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/categories',content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code==200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''


    #CREATE CATEGORY

    def test_items_category_no_admin_login(self):
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[0]) ,content_type='application/json')
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['msg'] == "Missing Authorization Header")
        assert(response.status_code==401)
    
    def test_items_category_description_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_items_category_name_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_category_both_name_and_description_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_category_name_not_str(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_items_category_both_name_and_description_filled(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[4]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_items_category_duplicate(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[4]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)


    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #GET SPECIFIC CATEGORY TESTS

    #BY ID

    def test_get_category_negative_identifier(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/categories/-1' ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(response.status_code == 404)

    def test_get_category_not_created(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/categories/100' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code == 404)

    def test_get_category_successfully(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.get('/api/v2/categories/2' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code == 200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

   
    #DELETE SPECIFIC CATEGORY TESTS

    #BY ID

    def test_delete_category_negative_identifier(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.delete('/api/v2/categories/-1' ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(response.status_code == 404)

    def test_delete_category_not_created(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.delete('/api/v2/categories/100' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code == 404)

   
    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #UPDATE CATEGORY

    def test_items_update_category_description_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.put('/api/v2/categories/2', data=json.dumps(sample_category_update[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_category_name_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.put('/api/v2/categories/2', data=json.dumps(sample_category_update[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_category_both_name_and_description_empty(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.put('/api/v2/categories/2', data=json.dumps(sample_category_update[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)

    def test_items_update_category_name_not_str(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.put('/api/v2/categories/2', data=json.dumps(sample_category_update[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    def test_items_update_category_both_name_and_description_filled(self):
        self.token = store_manager.sign_in_admin()
        response= self.test_client.put('/api/v2/categories/2', data=json.dumps(sample_category_update[4]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)

    

    '''-------------------------------------------------------------------------------------------------------------------------------'''
