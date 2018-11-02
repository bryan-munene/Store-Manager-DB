import unittest
import os
from flask import json
from app import create_app
from manage import DatabaseSetup

url = os.getenv('DATABASE_URL_TEST')


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
	        "password":"Adm1n234"
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


class Store_Manager_Base(unittest.TestCase):
    '''This class configures all the parameters needed for the tests and is inheritted by all other test classes.'''
    def setUp(self):
        '''This method sets up the necessary parameters such as the test client, test db and testing setting in the app'''
        self.app = create_app('testing')
        self.db = DatabaseSetup(url)
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.db.create_tables(url)
        self.db.create_default_admin_user(url)
        self.app.testing = True

        with self.app_context:
            self.app_context.push()
            
    def tearDown(self):
        '''This method clears all the data and records from the tests ran. It is ran at the end of the tests.'''
        with self.app_context:
            self.app_context.pop()
        self.db.drop_tables(url)

    def sign_up_user(self):
        '''
        this is a helper function for an ordinary user's registration
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        sign_up = self.test_client.post('/api/v2/register', data = json.dumps(sample_user[0]), content_type = 'application/json')
        assert (sign_up.status_code == 201)
        logout= self.test_client.get('/api/v2/logout', content_type = 'application/json')
        assert(logout.status_code == 200)
        
    def sign_in_user(self):
        '''
        this is a helper function for an ordinary user's login
        '''
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        sign_in = self.test_client.post('/api/v2/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
        assert (sign_in.status_code == 200)
    
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
        print(self.token)
        return self.token

    def add_items_helper(self):
        '''
        this is a helper function for adding items
        '''
        add_item = self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[0]) ,content_type='application/json', headers= self.token)
        assert(add_item.status_code==201)
        add_item = self.test_client.post('/api/v2/add_item', data=json.dumps(sample_item[1]) ,content_type='application/json', headers= self.token)
        assert(add_item.status_code==201)
        
    def make_sale_helper(self):
        '''
        this is a helper function to make a sale
        '''
        sell = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[0]) ,content_type='application/json', headers= self.token)
        assert(sell.status_code==201)
        