import pytest
import unittest
from flask import json

from .setup_tests import Store_Manager_Base

store_manager = Store_Manager_Base()

        
#REGISTRATION INPUT FOR TESTS

sample_registration = [
            {
            "name":"",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":""
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"testmail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass",
            "password2":"pass1"
            },
            {
            "name":"test",
            "email":"test@mail.com",
            "username":"tester2",
            "password":"pass11",
            "password2":"pass1"
            },
            {
            "name":"test",
            "email":"test_correct@mail.com",
            "username":"tester_correct",
            "password":"pass",
            "password2":"pass"
            }
        ]


#LOGIN CREDENTIALS FOR TESTS

sample_login = [
            {
            "email":"",	
            "password":"pass"
            },
            {
            "email":"test@adminmail.com",	
            "password":""
            },
            {
            "email":"testadminmail.com",	
            "password":"pass"
            },
            {
            "email":"test@adminmailcom",	
            "password":"pass"
            },
            {
            "email":"test@adminmail.com",	
            "password":"pass1"
            },
            {
            "email":"teste@mail.com",	
            "password":"pass1"
            },
            {
            "email":"test@adminmail.com",	
            "password":"Adm1n234"
            }
        ]

#SAMPLE DATA FOR USER UPDATE

sample_update = [
            {
            "name":"",
            "username":"tester2",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "username":"",
            "password":"pass",
            "password2":"pass"
            },
            {
            "name":"test",
            "username":"tester2",
            "password":"",
            "password2":"pass"
            },
            {
            "name":"test",
            "username":"tester2",
            "password":"pass",
            "password2":""
            },
            {
            "name":"test",
            "username":"tester2",
            "password":"pass",
            "password2":"pass1"
            },
            {
            "name":"test",
            "username":"tester2",
            "password":"pass11",
            "password2":"pass1"
            },
            {
            "name":"test",
            "username":"tester_correct_update",
            "password":"pass",
            "password2":"pass"
            }
        ]


class Test_Users(Store_Manager_Base):

    #LOGIN TESTS

    #INPUT CHECKS
    
        
    def test_login_empty_email(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[0]), content_type = 'application/json')
        assert(login.status_code == 406)

    def test_login_empty_password(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[1]), content_type = 'application/json')
        assert(login.status_code == 406)

    def test_login_wrong_email_format(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[2]), content_type = 'application/json')
        assert(login.status_code == 406)

    def test_login_wrong_email_format2(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[3]), content_type = 'application/json')
        assert(login.status_code == 404)


    #CREDENTIALS CHECK

    def test_login_wrong_password(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[4]), content_type = 'application/json')
        assert(login.status_code == 401)

    def test_login_wrong_email(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[5]), content_type = 'application/json')
        assert(login.status_code == 404)


    #CORRECT CREDENTIALS

    def test_login_correct_data(self):
        login = self.test_client.post('/api/v2/login', data = json.dumps(sample_login[6]), content_type = 'application/json')
        response = json.loads(login.data.decode('utf-8'))
        assert(response['status'] == "user logged in")
        assert(login.status_code == 200)


    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #REGISTRATION TESTS

    def test_register_without_admin_logged_in(self):
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[9]), content_type = 'application/json')
        response = json.loads(register.data.decode('utf-8'))
        assert(response['msg'] == "Missing Authorization Header")
        assert(register.status_code==401)
    
        
    #USER INPUT CHECKS
    
    def test_register_empty_name(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[0]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)

    def test_register_empty_email(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[1]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)

    def test_register_empty_username(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[2]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)

    def test_register_empty_password(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[3]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)

    def test_register_empty_password2(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[4]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)


    #EMAIL FORMAT CHECKS

    def test_register_wrong_email_format1(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[6]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)


    #PASSWORD CHECK

    def test_register_passwords_matching(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[7]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)

    def test_register_passwords_matching1(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[8]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(register.status_code == 406)


    #CORRECT INPUT

    def test_register_correct_data(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[9]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "created")
        assert (register.status_code == 201)


    #DUPLICATE INPUT

    def test_register_duplicate_input(self):
        self.token = store_manager.sign_in_admin()
        register = self.test_client.post('/api/v2/register', data = json.dumps(sample_registration[9]), content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(register.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert (register.status_code == 406)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #LOGOUT TESTS

    def test_logout_correctly(self):
        self.token = store_manager.sign_in_admin()
        logout= self.test_client.delete('/api/v2/logout', content_type = 'application/json', headers=dict(Authorization=self.token))
        response = json.loads(logout.data.decode('utf-8'))
        assert(response['status'] == "logged out")
        assert(logout.status_code == 200)

    def test_logout_without_logged_in(self):
        logout= self.test_client.delete('/api/v2/logout', content_type = 'application/json')
        response = json.loads(logout.data.decode('utf-8'))
        assert(response['msg'] == "Missing Authorization Header")
        assert(logout.status_code==401)


    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #GET ALL USERS TEST


    def test_users_retrive_all_no_admin_login(self):
        get= self.test_client.get('/api/v2/users',content_type='application/json')
        response = json.loads(get.data.decode('utf-8'))
        assert(response['msg'] == "Missing Authorization Header")
        assert(get.status_code==401)


    def test_users_retrive_all_successfully(self):
        self.token = store_manager.sign_in_admin()
        get= self.test_client.get('/api/v2/users',content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(get.data.decode('utf-8'))
        assert(response['status'] == "ok")
        assert(get.status_code==200)


    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #GET SPECIFIC USER TEST


    def test_users_retrive_user_no_admin_login(self):
        get= self.test_client.get('/api/v2/users/1',content_type='application/json')
        response = json.loads(get.data.decode('utf-8'))
        assert(response['msg'] == "Missing Authorization Header")
        assert(get.status_code==401)

    def test_users_retrive_user_not_created(self):
        self.token = store_manager.sign_in_admin()
        get= self.test_client.get('/api/v2/users/100',content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(get.data.decode('utf-8'))
        assert(response['status'] == "not found")
        assert(get.status_code==404)

    def test_users_retrive_user_negative_id(self):
        self.token = store_manager.sign_in_admin()
        get= self.test_client.get('/api/v2/users/-1',content_type='application/json', headers=dict(Authorization=self.token))
        assert(get.status_code==404)

    def test_users_retrive_user_successfully(self):
        self.token = store_manager.sign_in_admin()
        get= self.test_client.get('/api/v2/users/1',content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(get.data.decode('utf-8'))
        assert(response['status'] == "ok")
        assert(get.status_code==200)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #UPDATE SPECIFIC USER TEST


    def test_users_update_user_no_admin_login(self):
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[6]), content_type='application/json')
        response = json.loads(update.data.decode('utf-8'))
        assert(response['msg'] == "Missing Authorization Header")
        assert(update.status_code==401)

    def test_users_update_user_not_created(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/100', data = json.dumps(sample_update[6]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not found")
        assert(update.status_code==404)

    def test_users_update_user_negative_id(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/-2', data = json.dumps(sample_update[6]), content_type='application/json', headers=dict(Authorization=self.token))
        assert(update.status_code==404)

    def test_users_update_user_empty_name(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[0]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(update.status_code==406)
    
    def test_users_update_user_empty_username(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[1]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(update.status_code==406)
    
    def test_users_update_user_empty_password(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[2]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(update.status_code==406)

    def test_users_update_user_empty_password2(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[3]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(update.status_code==406)

    def test_users_update_user_password_match(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[4]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(update.status_code==406)

    def test_users_update_user_password_match2(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[5]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "not acceptable")
        assert(update.status_code==406)

    def test_users_update_user_successfully(self):
        self.token = store_manager.sign_in_admin()
        update= self.test_client.put('/api/v2/users/2', data = json.dumps(sample_update[6]), content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(update.data.decode('utf-8'))
        assert(response['status'] == "created")
        assert(update.status_code==201)

    '''-------------------------------------------------------------------------------------------------------------------------------'''

    #DELETE SPECIFIC USER TEST


    def test_users_delete_user_no_admin_login(self):
        delete= self.test_client.delete('/api/v2/users/2',content_type='application/json')
        response = json.loads(delete.data.decode('utf-8'))
        assert(response['msg'] == "Missing Authorization Header")
        assert(delete.status_code==401)

    def test_users_delete_user_not_created(self):
        self.token = store_manager.sign_in_admin()
        delete= self.test_client.delete('/api/v2/users/100',content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(delete.data.decode('utf-8'))
        assert(response['status'] == "not found")
        assert(delete.status_code==404)

    def test_users_delete_user_negative_id(self):
        self.token = store_manager.sign_in_admin()
        delete= self.test_client.delete('/api/v2/users/-1',content_type='application/json', headers=dict(Authorization=self.token))
        assert(delete.status_code==404)

    def test_users_delete_user_successfully(self):
        self.token = store_manager.sign_in_admin()
        delete= self.test_client.delete('/api/v2/users/2',content_type='application/json', headers=dict(Authorization=self.token))
        response = json.loads(delete.data.decode('utf-8'))
        assert(response['status'] == "ok")
        assert(delete.status_code==200)
