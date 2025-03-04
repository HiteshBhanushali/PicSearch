import os
import json
import uuid
from PIL import Image
from models.git_model import GITModel
from config import Config
from utils.embeddings import EmbeddingModel
from concurrent.futures import ThreadPoolExecutor

class ImageAnalyzer:
    def __init__(self):
        self.git_model = GITModel()
        self.embedding_model = EmbeddingModel()
        self.json_file = Config.JSON_DATA_FILE
        self.executor = ThreadPoolExecutor(max_workers=4)  # Adjust the number of workers as needed
    
    def save_image(self, image_file):
        """Save uploaded image to storage and return the path"""
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.{image_file.filename.split('.')[-1].lower()}"
        save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        # Save the file
        image_file.save(save_path)
        
        # Return relative path for storage in JSON
        return os.path.join('static', 'uploads', filename)
    
    def analyze_image(self, image_path):
        """Generate detailed description for an image"""
        try:
            # Convert relative path to absolute for processing
            abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), image_path)
            
            # Open image file
            image = Image.open(abs_path)
            
            # Generate description
            description = self.git_model.generate_description(image)
            
            return description
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return "Failed to analyze image."
    
    def save_description(self, image_path, description):
        """Save image description to JSON file"""
        try:
            # Generate embedding for the description
            embedding = self.embedding_model.get_embedding(description).tolist()
            
            # Create entry
            entry = {
                "image_path": image_path,
                "description": description,
                "embedding": embedding,
                "id": str(uuid.uuid4())
            }
            
            # Load existing data
            data = []
            if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
                with open(self.json_file, 'r') as f:
                    data = json.load(f)
            
            # Add new entry
            data.append(entry)
            
            # Save updated data
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error saving description: {str(e)}")
            return False
    
    def process_image(self, image_file):
        """Process a single image and save its description"""
        try:
            # Save image
            image_path = self.save_image(image_file)
            
            # Analyze image
            description = self.analyze_image(image_path)
            
            # Save description
            success = self.save_description(image_path, description)
            
            return {
                "image_path": image_path,
                "description": description,
                "success": success
            }
        except Exception as e:
            print(f"Error processing image {image_file.filename}: {str(e)}")
            return {
                "image_path": None,
                "description": None,
                "success": False,
                "error": str(e)
            }
    
    def process_images(self, image_files):
        """Process multiple images and save their descriptions"""
        results = list(self.executor.map(self.process_image, image_files))
        return results
    
    def search_images(self, query, limit=10):
        """Search for images based on query text"""
        try:
            # Load existing data
            data = []
            if os.path.exists(self.json_file) and os.path.getsize(self.json_file) > 0:
                with open(self.json_file, 'r') as f:
                    data = json.load(f)
            
            # Perform semantic search
            results = self.embedding_model.semantic_search(query, data, top_k=limit)
            
            return results
        except Exception as e:
            print(f"Error searching images: {str(e)}")
            return []