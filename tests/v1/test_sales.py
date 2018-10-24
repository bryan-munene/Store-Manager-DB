import pytest
from flask import json
from app import create_app
from app.api.v1.views.items import Items
from app.api.v1.views.sales import Sales
from app.api.v1.views.auth import Users
from tests.test_helpers import make_sale_helper, sign_in_admin_helper, sign_in_helper, sign_in_helper_2, add_items_helper

testitems = Items()
testsales = Sales()
testusers = Users()
app = create_app(config="testing")

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

#GET ALL SALES TESTS


def test_sales_retrive_all_no_sale():
    test_client = app.test_client()
    response = test_client.get('/api/v1/sales',content_type='application/json')
    assert(response.status_code==404)
    

def test_sales_retrive_all_successfully():
    test_client = app.test_client()
    make_sale_helper(test_client)
    response = test_client.get('/api/v1/sales',content_type='application/json')
    assert(response.status_code==200)
    
'''-------------------------------------------------------------------------------------------------------------------------------'''

#MAKE A SALE TESTS


def test_sales_quantity_not_digit():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[0]) ,content_type='application/json')
    assert(response.status_code==400)
    

def test_sales_item_id_not_digit():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[1]) ,content_type='application/json')
    assert(response.status_code==400)
    

def test_sales_item_id_empty():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[2]) ,content_type='application/json')
    assert(response.status_code==406)
    

def test_sales_quantity_empty():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[3]) ,content_type='application/json')
    assert(response.status_code==406)


def test_sales_quantity_more_than_available_stock():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[4]) ,content_type='application/json')
    assert(response.status_code==406)


def test_sales_payment_method_empty():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[5]) ,content_type='application/json')
    assert(response.status_code==406)
    

def test_sales_sale_items_empty():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[6]) ,content_type='application/json')
    assert(response.status_code==406)
    

def test_place_sale_successfully():
    test_client = app.test_client()
    response = test_client.post('/api/v1/make_sale', data=json.dumps(sample_sale[7]) ,content_type='application/json')
    json.loads(response.data)
    assert(response.status_code==201)
    

'''-------------------------------------------------------------------------------------------------------------------------------'''

#GET SPECIFIC SALE TESTS


def test_get_sale_negative_identifier():
    test_client = app.test_client()
    response = test_client.get('/api/v1/sales/-1' ,content_type='application/json')
    assert(response.status_code == 404)


def test_get_sale_not_created():
    test_client = app.test_client()
    response = test_client.get('/api/v1/sales/100' ,content_type='application/json')
    assert(response.status_code == 404)

def test_get_sale_successfully():
    test_client = app.test_client()
    make_sale_helper(test_client)
    response = test_client.get('/api/v1/sales/1' ,content_type='application/json')
    assert(response.status_code == 200)

'''-------------------------------------------------------------------------------------------------------------------------------'''

