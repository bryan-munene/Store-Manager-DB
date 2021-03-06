import unittest
import os
from flask import json
from app import create_app
from instance.config import app_config
from manage import DatabaseSetup




sample_user=[
            {
            "name":"test",
            "email":"test_details@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "email":"test_details@mail.com",	
            "password":"pass"
            },
            {
            "email":"test@adminmail.com", 
	        "password":"Adm1n234"
            }
]


sample_item = [
    {
	"name":"Panadol", 
	"price":"220",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"Amoxil", 
	"price":"200",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"items", 
	"price":"220",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    },
    {
	"name":"item", 
	"price":"200",	
	"image":"image", 
	"quantity":"12", 
	"reorder_point":"3", 
	"category_id":"1"
    }
]

sample_category = [
    {"name":"painkillers3", "description":"alleviates pain"},
    {"name":"painkillers4", "description":"alleviates pain"},
    {"name":"painkillers5", "description":"alleviates pain"},
    {"name":"painkillers6", "description":"alleviates pain"}
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


class Store_Manager_Base(unittest.TestCase):
    '''This class configures all the parameters needed for the tests and is inheritted by all other test classes.'''
    db = DatabaseSetup('testing')
    db.drop_tables()

    def setUp(self):
        '''This method sets up the necessary parameters such as the test client, test db and testing setting in the app'''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        with self.app_context:
            self.app_context.push()
             
    def tearDown(self):
        '''This method clears all the data and records from the tests ran. It is ran at the end of the tests.'''
        self.app_context.pop()
        
            
    def sign_up_user(self):
        '''
        this is a helper function for an ordinary user's registration
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.token = self.sign_in_admin()
        sign_up = self.test_client.post('/api/v2/register', data = json.dumps(sample_user[0]), content_type = 'application/json', headers=dict(Authorization=self.token))
        assert (sign_up.status_code == 201)
                
    def sign_in_user(self):
        '''
        this is a helper function for an ordinary user's login
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        sign_in = self.test_client.post('/api/v2/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
        data = json.loads(sign_in.data.decode('utf-8'))
        assert (sign_in.status_code == 200)
        self.token = "Bearer " + data['token']
        return self.token
    
    def sign_in_admin(self):
        '''
        this is a helper function for an admin user's login
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        sign_in = self.test_client.post('/api/v2/login', data = json.dumps(sample_user[2]), content_type = 'application/json')
        data = json.loads(sign_in.data.decode('utf-8'))
        assert (sign_in.status_code == 200)
        self.token = "Bearer " + data['token']
        return self.token

    def add_category_helper(self):
        '''
        this is a helper function for adding categories
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.token = self.sign_in_admin()
        add_category = self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_category.status_code==201)
        add_category = self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_category.status_code==201)
        add_category = self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_category.status_code==201)
        add_category = self.test_client.post('/api/v2/add_category', data=json.dumps(sample_category[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_category.status_code==201)
        
    def add_items_helper(self):
        '''
        this is a helper function for adding items
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.token = self.sign_in_admin()
        self.add_category_helper()
        add_item = self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_item.status_code==201)
        add_item = self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_item.status_code==201)
        add_item = self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_item.status_code==201)
        add_item = self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(add_item.status_code==201)
        
    def make_sale_helper(self):
        '''
        this is a helper function to make a sale
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.token = self.sign_in_user()
        sell = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(sell.status_code==201)
        