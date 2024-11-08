from flask import Flask
import os
from flask_cors import CORS
from flask_pymongo import PyMongo

#initializing app
app = Flask(__name__)
CORS(app)

app.config.from_object('config.Config')
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
## init mongodb
mongo = PyMongo(app)

#init functions
def register_bps():

    from lib.routes.customers.customers import customers_bp
    app.register_blueprint(customers_bp)

    from lib.routes._test.test import test_bp
    app.register_blueprint(test_bp)

if __name__ == '__main__':
    register_bps()
    app.run(debug=True)


# entry route
@app.route('/')
def home():
    return "Welcome to my app! ABT web application"
