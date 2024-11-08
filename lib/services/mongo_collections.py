from flask_pymongo import PyMongo as pymongo
from pymongo.collection import Collection

class MongoCollections:

    TEST="test"
    SITES="sites"
    CUSTOMERS="customers"

    @staticmethod
    def get_collection_instance(key: str) -> Collection:

        from app import mongo
        
        if key == MongoCollections.TEST:
            return mongo.db.test
        elif key == MongoCollections.SITES:
            return mongo.db.sites  
        elif key == MongoCollections.CUSTOMERS:
            return mongo.db.customers    
        else:
            return mongo.db.test
