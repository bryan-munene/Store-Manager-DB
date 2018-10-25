# import the flask app from the function that creates it.
from app import create_app

# set the necessary config enviroment from the config.py file
CONFIG_TYPE = "development"
app = create_app(CONFIG_TYPE)

if __name__ == '__main__':  # run the flask app
    app.run()
