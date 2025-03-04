import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
from utils.image_analyzer import analyze_image
from utils.embeddings import generate_embeddings
import models.git_model as git_model

app = Flask(__name__)
CORS(app)

# Configure environment variables
PORT = int(os.environ.get("PORT", 10000))
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return jsonify({"status": "API is running"})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze image
        analysis = analyze_image(filepath)
        
        # Generate embeddings
        embedding = generate_embeddings(analysis["description"])
        
        # Save to data file
        data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/image_descriptions.json")
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        data.append({
            "filename": filename,
            "description": analysis["description"],
            "embedding": embedding,
            "tags": analysis["tags"]
        })
        
        with open(data_file, 'w') as f:
            json.dump(data, f)
        
        return jsonify({
            "filename": filename,
            "description": analysis["description"],
            "tags": analysis["tags"]
        })

@app.route('/api/search', methods=['POST'])
def search_images():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    # Generate embedding for the query
    query_embedding = generate_embeddings(query)
    
    # Use model to find similar images
    results = git_model.find_similar_images(query_embedding)
    
    return jsonify({"results": results})

@app.route('/api/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)