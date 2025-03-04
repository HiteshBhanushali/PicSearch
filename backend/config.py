import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration class
class Config:
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    JSON_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'image_descriptions.json')
    
    # Allowed image file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Model settings
    GIT_MODEL_NAME = "microsoft/git-large"
    SBERT_MODEL_NAME = "all-MiniLM-L6-v2"  # Lightweight model for sentence embeddings
    
    # Create necessary directories if they don't exist
    @staticmethod
    def init_app():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.JSON_DATA_FILE), exist_ok=True)
        
        # Create an empty JSON file if it doesn't exist
        if not os.path.exists(Config.JSON_DATA_FILE):
            with open(Config.JSON_DATA_FILE, 'w') as f:
                f.write('[]')