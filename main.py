print("Hello")

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Access MongoDB URI from environment variable
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["mydatabase"]
collection = db["items"]

# API endpoints as before
@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    item_data = request.json
    collection.insert_one(item_data)
    return jsonify({"message": "Item added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
