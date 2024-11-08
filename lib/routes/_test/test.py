from flask import Blueprint, jsonify, request
from lib.services.google_drive_service import GoogleDriveService
from lib.services.response_util import create_response

test_bp = Blueprint('test', __name__)

# Route to create a document in MongoDB
@test_bp.route('/test', methods=['POST','GET'])
def upload_file():

    google_drive = GoogleDriveService()

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_id, file_url = google_drive.upload_to_drive(file)

    if file_id:
        return create_response(success=True,message=file_url)
    else:
        return create_response(success=False)
    
