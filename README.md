# Store-Manager-DB

![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Build Status](https://travis-ci.org/bryan-munene/Store-Manager-DB.svg?branch=develop)](https://travis-ci.org/bryan-munene/Store-Manager-DB)
[![codecov](https://codecov.io/gh/bryan-munene/Store-Manager-DB/branch/develop/graph/badge.svg)](https://codecov.io/gh/bryan-munene/Store-Manager-DB)
[![Maintainability](https://api.codeclimate.com/v1/badges/f0adf3f5a8c1ca0fbfd2/maintainability)](https://codeclimate.com/github/bryan-munene/Store-Manager-DB/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f0adf3f5a8c1ca0fbfd2/test_coverage)](https://codeclimate.com/github/bryan-munene/Store-Manager-DB/test_coverage)

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store. This is an implementation using a database.


# Features.

1. Store attendant can search and add products to buyer’s cart.
2. Store attendant can see his/her sale records but can’t modify them.
3. App should show available products, quantity and price.
4. Store owner can see sales and can filter by attendants.
5. Store owner can add, modify and delete products.
6. Store owner can give admin rights to a store attendant.
7. Products should have categories.
8. Store attendants should be able to add products to specific categories.
9. Store owner can give admin rights to a store attendant.
10. Products should have categories.
11. Store attendants should be able to add products to specific categories.


## Getting Started

These instructions will guid you on how to deploy this system locally. For live systems, you will need to consult deployment notes of flask systems for that.

To get started first you need a machine that can run on Python3 and handle postgres database.

### Prerequisites

You will need these installed first before we go any further.

- [Python3.6](https://www.python.org/downloads/release/python-365/)

- [Virtual Environment](https://virtualenv.pypa.io/en/stable/installation/)

- [Postgresql Database](https://www.postgresql.org/)

Create a Database ```store_manager``` for your app
and ```store_manager_test``` for your tests

For Virtual Environment, you can install like this after Installing Python3:

```
pip install virtualenv
```
```
pip install virtualenvwrapper
```


## Installation and Running


### Installing

Clone the repository below

```
git clone -b development https://github.com/bryan-munene/Store-Manager-DB.git
```

Create a virtual environment

```
    virtualenv venv --python=python3.6
```

Activate virtual environment

On Linux:

```
    source venv/bin/activate
```

On Windows:

```
    venv\Scripts\activate
```

Install required Dependencies

```
    pip install -r requirements.txt
```



### Running

Start the flask server on your command prompt:

    First you need to ``` cd ``` to your project root directory

#### Create a .env file

On Linux:

    ```$ touch .env```

Set the environment variables

```
    - export FLASK_APP="run.py"
    - export APP_SETTINGS="development"
    - export DATABASE_URL=host='localhost' port='5432' user='postgres' password='root' dbname='store_manager'
    - export DATABASE_URL_TEST=host='localhost' user='postgres' password='root' dbname='store_manager_test'
    - export SECRET_KEY=" \87b\0ha\j&^\*kd\fg4\ugy\8gq\4tt\0nj\bga\g$%\^&*\()d\l*7\*&^\&$%\bjd\bnj\bns\236\7$%\^&*\()i\nkn\fgs\dgj\n4k\*&6\%gb\hbj\fgh\}|{\POI\IUP\{O}\dhf\jhb\$%^\&*(\!@#\$@!\@#{\}{{\}:{\LMk\ "

```

On Windows:

Set the environment variables

```
    - set FLASK_APP="run.py"
    - set APP_SETTINGS="development"
    - set DATABASE_URL=host='localhost' port='5432' user='postgres' password='root' dbname='store_manager'
    - set DATABASE_URL_TEST=host='localhost' user='postgres' password='root' dbname='store_manager_test'
    - set SECRET_KEY=" \87b\0ha\j&^\*kd\fg4\ugy\8gq\4tt\0nj\bga\g$%\^&*\()d\l*7\*&^\&$%\bjd\bnj\bns\236\7$%\^&*\()i\nkn\fgs\dgj\n4k\*&6\%gb\hbj\fgh\}|{\POI\IUP\{O}\dhf\jhb\$%^\&*(\!@#\$@!\@#{\}{{\}:{\LMk\ "

```


Then:

```
    python run.py
```

With the server running, paste this in your browser's address bar:

```
    localhost:5000/api/v2/
```

This is the welcome page.



## Running the tests

This repository contains tests to test the functionality of the API.

To run these tests, run the following command:

### Running all tests.

    These tests test the ``` Items Class, Sales Class, Categories Class and the Users Class```

In the project's root directory, with the virtual environment running, run this command:

```
pytest
```


### Running specific test scripts

It is possible to run test scripts individually. 

    You need to ``` cd ``` to your tests directory.

```
pytest test_auth.py
```
to test the class Users only.


# Versioning

This app contains multiple versions.

**Version 1** uses python data structures (non-persistent storage), to store the data.

**Version 2** is made up of the following endpoints and uses postgresql database to store data.

# Endpoints

## Version 1 Endpoints Available

|    #   | Method | Endpoint                            | Description                           |
|--------| ------ | ----------------------------------- | ------------------------------------- |
|    1   | GET    | /api/v2/                            | Index/Welcome page                    |
|    2   | POST   | /api/v2/register                    | Create new user                       |
|    3   | POST   | /api/v2/login                       | Login a registered user               |
|    4   | GET    | /api/v2/users                       | Retrieve all users                    |
|    5   | GET    | /api/v2/users/<int:user_id>         | Retrieve a specific user              |
|    6   | PUT    | /api/v2/users/<int:user_id>         | Update a user                         |
|    7   | DELETE | /api/v2/users/<int:user_id>         | Delete a user                         |
|    8   | PUT    | /api/v2/role/<int:user_id>          | Update a user's role                  |
|    9   | DELETE | /api/v2/logout                      | Logout a logged in user               |
|    10  | POST   | /api/v2/add_category                | Add a category                        |
|    11  | GET    | /api/v2/categories                  | Retrieve all categories               |
|    12  | GET    | /api/v2/categories/<int:category_id>| Retrieve a specific category          |
|    13  | PUT    | /api/v2/categories/<int:category_id>| Update a category                     |
|    14  | DELETE | /api/v2/categories/<int:category_id>| Delete a category                     |
|    15  | POST   | /api/v2/add_item                    | Create a new item                     |
|    16  | GET    | /api/v2/items                       | Retrieve all items                    |
|    17  | GET    | /api/v2/items/<int:item_id>         | Retrieve a specific item by item id   |
|    18  | PUT    | /api/v2/items/<int:item_id>         | Update an item                        |
|    19  | DELETE | /api/v2/items/<int:item_id>         | Delete an item                        |
|    20  | PUT    | /api/v2/stock/<int:item_id>         | Update an item's stock                |
|    21  | POST   | /api/v2/make_sale                   | Make a sale                           |
|    22  | GET    | /api/v2/sales                       | Retrieve all sales                    |
|    23  | GET    | /api/v2/sales/<sale_id>             | Retrieve a specific sale              |


# Documentation

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b9518e79588f0fc7bbdf#?env%5BStore%20Manager%5D=W10=)

[Store Manger API Documentation](https://documenter.getpostman.com/view/4618681/RzZ4ogck)



# Deployment

This app is deployed [here](https://bmmstoreman-db-heroku.herokuapp.com/api/v2)


## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [pip](https://pypi.org/project/pip/) - Dependency Management


## Authors

* [Muthuri Munene Bryan](https://github.com/bryan-munene)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details

