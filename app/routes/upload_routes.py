import os
from flask import Blueprint, request, jsonify, current_app
from app.services.file_processing_service import FileProcessingService

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

# Define a temporary folder for uploads before they are routed
TEMP_UPLOAD_FOLDER = "temp_uploads"
os.makedirs(TEMP_UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    success, message = FileProcessingService.process_file(file, TEMP_UPLOAD_FOLDER)
    
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
