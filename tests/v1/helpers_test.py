import pytest
import unittest
from flask import json
from .setup_tests import Store_Manager_Base

store_manager = Store_Manager_Base()



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



class Helpers(Store_Manager_Base):
    '''This class holds helper methods for tests'''    
    def sign_up_user(self):
        '''
        this is a helper function for an ordinary user's registration
        '''
        sign_up = self.test_client.post('/api/v2/register', data = json.dumps(sample_user[0]), content_type = 'application/json')
        assert (sign_up.status_code == 201)
        logout= self.test_client.get('/api/v2/logout', content_type = 'application/json')
        assert(logout.status_code == 200)
        
    def sign_in_user(self):
        '''
        this is a helper function for an ordinary user's login
        '''
        sign_in = self.test_client.post('/api/v2/login', data = json.dumps(sample_user[1]), content_type = 'application/json')
        assert (sign_in.status_code == 200)
    
    def sign_in_admin(self):
        '''
        this is a helper function for an admin user's login
        '''
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
        
