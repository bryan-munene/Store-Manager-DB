import pytest
import unittest
from flask import json
from .setup_tests import Store_Manager_Base

store_manager = Store_Manager_Base()


#ORDER INPUT FOR TESTS

sample_sale=[{
            "payment_mode":"Cash",
            "sale_items": [
    	                    {
    		                "item_id":"1",
    		                "quantity":"abc"
    	                    },
    	                    {
    		                "item_id":"2",
    		                "quantity":"def"
    	                    }
                           ]
            },
            {
            "payment_mode":"Cash",
            "sale_items": [
    	                    {
    		                "item_id":"Panadol",
    		                "quantity":"4"
    	                    },
    	                    {
    		                "item_id":"Amoxil",
    		                "quantity":"9"
    	                    }
                           ]
            },
            {
            "payment_mode":"Cash",
            "sale_items": [
    	                    {
    		                "item_id":"",
    		                "quantity":"4"
    	                    },
    	                    {
    		                "item_id":"",
    		                "quantity":"9"
    	                    }
                           ]
            },
            {
            "payment_mode":"Cash",
            "sale_items": [
    	                    {
    		                "item_id":"1",
    		                "quantity":""
    	                    },
    	                    {
    		                "item_id":"2",
    		                "quantity":""
    	                    }
                           ]
            },
            {
            "payment_mode":"Cash",
            "sale_items": [
    	                    {
    		                "item_id":"1",
    		                "quantity":"40"
    	                    },
    	                    {
    		                "item_id":"2",
    		                "quantity":"90"
    	                    }
                           ]
            },
            {
            "payment_mode":"",
            "sale_items": [
    	                    {
    		                "item_id":"1",
    		                "quantity":"4"
    	                    },
    	                    {
    		                "item_id":"2",
    		                "quantity":"9"
    	                    }
                           ]
            },
            {
            "payment_mode":"Cash",
            "sale_items": []
            },
            {
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


'''-------------------------------------------------------------------------------------------------------------------------------'''
class Test_Sales(Store_Manager_Base):

    #SALES
    
    #GET ALL SALES TESTS


    def test_sales_retrive_all_no_sale(self):
        self.token = self.sign_in_admin()
        response = self.test_client.get('/api/v2/sales',content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code==404)
        

    def test_sales_retrive_all_successfully(self):
        self.token = self.sign_in_admin()
        response = self.test_client.get('/api/v2/sales',content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code==200)
        
    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #MAKE A SALE TESTS


    def test_sales_quantity_not_digit(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[0]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)
        

    def test_sales_item_id_not_digit(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[1]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)
        

    def test_sales_item_id_empty(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[2]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)
        

    def test_sales_quantity_empty(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[3]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)


    def test_sales_quantity_more_than_available_stock(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[4]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)


    def test_sales_payment_method_empty(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[5]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)
        

    def test_sales_sale_items_empty(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[6]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not acceptable")
        assert(response.status_code==406)
        

    def test_place_sale_successfully(self):
        self.token = self.sign_in_user()
        response = self.test_client.post('/api/v2/make_sale', data=json.dumps(sample_sale[7]) ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "created")
        assert(response.status_code==201)
        

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #GET SPECIFIC SALE TESTS


    def test_get_sale_negative_identifier(self):
        self.token = self.sign_in_admin()
        response = self.test_client.get('/api/v2/sales/-1' ,content_type='application/json', headers=dict(Authorization=self.token))
        assert(response.status_code == 404)


    def test_get_sale_not_created(self):
        self.token = self.sign_in_admin()
        response = self.test_client.get('/api/v2/sales/100' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "not found")
        assert(response.status_code == 404)

    def test_get_sale_successfully(self):
        self.token = self.sign_in_admin()
        response = self.test_client.get('/api/v2/sales/1' ,content_type='application/json', headers=dict(Authorization=self.token))
        msg = json.loads(response.data.decode('utf-8'))
        assert(msg['status'] == "ok")
        assert(response.status_code == 200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    