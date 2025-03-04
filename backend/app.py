import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from utils.image_analyzer import ImageAnalyzer

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app()
CORS(app)

# Initialize image analyzer
image_analyzer = ImageAnalyzer()

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload', methods=['POST'])
def upload_images():
    """Upload and analyze images"""
    if 'images' not in request.files:
        return jsonify({"error": "No images provided"}), 400
    
    # Get the list of image files
    image_files = request.files.getlist('images')
    
    # Validate files
    valid_images = []
    for image_file in image_files:
        if image_file and allowed_file(image_file.filename):
            valid_images.append(image_file)
    
    if not valid_images:
        return jsonify({"error": "No valid images provided"}), 400
    
    # Process images
    results = image_analyzer.process_images(valid_images)
    
    return jsonify({"results": results})

@app.route('/api/search', methods=['GET'])
def search_images():
    """Search for images based on query text"""
    query = request.args.get('query', '')
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Search for images
    results = image_analyzer.search_images(query, limit=limit)
    
    return jsonify({"results": results})

@app.route('/api/all_images', methods=['GET'])
def get_all_images():
    """Get all images and their descriptions"""
    try:
        # Load data from JSON file
        with open(Config.JSON_DATA_FILE, 'r') as f:
            data = json.load(f)
        
        # Remove embedding data to reduce payload size
        for item in data:
            if 'embedding' in item:
                del item['embedding']
        
        return jsonify({"images": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)