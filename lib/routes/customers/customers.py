from bson import ObjectId
from flask import Blueprint, request, jsonify
from lib.services.response_util import create_response
from lib.services.mongo_collections import MongoCollections
from lib.models.customer_model import ModelSchema as customer_schema
from lib.services.app_util import AppUtils

customers_bp = Blueprint('customers', __name__)

    
@customers_bp.route('/customers', methods=['POST'])
def post_a_document():
    data = request.json
    if not data:
        return create_response(
            data=None,
            success=False,
            status_code=400,
            message= "No data!"
        )
    
    #validation
    result = AppUtils.validate_schema(customer_schema(),data)

    if(result != None):
        return create_response(
            data=str(result),
            success=False,
            status_code=400,
            message= "Validation Error"
        )
       
    # Save the document to the MongoDB collection
    try:
        col = MongoCollections.get_collection_instance(MongoCollections.CUSTOMERS)
        col.insert_one(data)
        return create_response(
            data=None,
            success=True,
            status_code=201,
            message= "A document has been created successfully!"
        )
    except Exception as e:
        print(e)
        return create_response(
            data=None,
            success=False,
            status_code=500,
            message= e
        )    

@customers_bp.route('/customers', methods=['GET'])
def fetch_documents():
    try:
        documents = MongoCollections.get_collection_instance(MongoCollections.CUSTOMERS).find()
      
        result = []
        for doc in documents:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
            result.append(doc)

        return create_response(
            success=True,
            status_code=200,
            data=result,
        )
    
    except Exception as e:
        return create_response(
            data=None,
            success=False,
            status_code=500,
            message= e
        )


@customers_bp.route('/customers/<customer_id>', methods=['GET'])
def fetch_a_document_by_id(customer_id):

    try:
        col = MongoCollections.get_collection_instance(MongoCollections.CUSTOMERS)
        print("========"+ str("Start"))
        db_result = col.find_one(
            filter={"_id": ObjectId(customer_id)},
        )
        print("========"+ str(db_result))
        if(db_result==None): raise ValueError("No record")
        print("========"+ str(db_result))
        db_result["_id"] = str(db_result["_id"])
        return create_response(
            data= db_result,
            success=True,
            status_code=203,
            message= "The document has been updated successfully!"
        )
    except Exception as e:
        return create_response(
            data=None,
            success=False,
            status_code=500,
            message= str(e)
        )    

@customers_bp.route('/customers/<customer_id>', methods=['PUT'])
def update_document(customer_id):
    data = request.json
    if not data:
        return create_response(
            data=None,
            success=False,
            status_code=400,
            message= "No data!"
        )
    
    #validation
    result = AppUtils.validate_schema(customer_schema(),data)

    if(result != None):
        return create_response(
            data=str(result),
            success=False,
            status_code=400,
            message= "Validation Error")
    

    #edit document
    try:
        col = MongoCollections.get_collection_instance(MongoCollections.CUSTOMERS)
        db_result = col.update_one(
            filter={"_id": ObjectId(customer_id)},  # Convert the customer_id to ObjectId
            update={"$set": data}  # Use $set to update fields
        )
        return create_response(
            data= str(db_result.raw_result),
            success=True,
            status_code=203,
            message= "The document has been updated successfully!"
        )
    except Exception as e:
        return create_response(
            data=None,
            success=False,
            status_code=500,
            message= e
        )    
    
@customers_bp.route('/customers/<customer_id>', methods=['DELETE'])
def delete_document_by_id(customer_id):
    try:
        # Get the collection instance
        col = MongoCollections.get_collection_instance(MongoCollections.CUSTOMERS)

        # Attempt to delete the document by _id
        result = col.delete_one({"_id": ObjectId(customer_id)})

        # If no document was deleted, raise an error
        if result.deleted_count == 0:
            raise ValueError("No record found to delete")
        
        # Return success response
        return create_response(
            data=None,
            success=True,
            status_code=200,  # HTTP OK
            message="Document deleted successfully"
        )
    except ValueError as e:  # Catch ValueError separately
        print(e)
        return create_response(
            data=None,
            success=False,
            status_code=404,  # Not Found
            message=str(e)
        )
    except Exception as e:
        print(e)
        return create_response(
            data=None,
            success=False,
            status_code=500,  # Internal Server Error
            message="An error occurred while deleting the document"
        )