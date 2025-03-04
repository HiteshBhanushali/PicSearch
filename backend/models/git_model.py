import os
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from config import Config

class GITModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GITModel, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.processor = None
            cls._instance.device = "cuda" if torch.cuda.is_available() else "cpu"
        return cls._instance
    
    def load_model(self):
        
        if self.model is None or self.processor is None:
            model_path = Config.GIT_MODEL_NAME
            
            # Check if model exists locally
            if os.path.exists('./models/git-large'):
                model_path = './models/git-large'
                print(f"Loading GIT model from local path: {model_path}")
            else:
                print(f"Downloading GIT model: {model_path}")
                
            try:
                self.processor = AutoProcessor.from_pretrained(model_path)
                self.model = AutoModelForCausalLM.from_pretrained(model_path)
                
                # Move model to GPU if available
                self.model.to(self.device)
                
                # Save locally if downloaded from Hub
                if model_path == Config.GIT_MODEL_NAME:
                    os.makedirs('./models/git-large', exist_ok=True)
                    self.processor.save_pretrained('./models/git-large')
                    self.model.save_pretrained('./models/git-large')
                    
                print("GIT model loaded successfully")
            except Exception as e:
                print(f"Error loading GIT model: {str(e)}")
                raise
    
    def generate_description(self, image_path):
        """Generate a detailed description of the provided image"""
        if self.model is None or self.processor is None:
            self.load_model()
        
        try:
            # Process the image
            inputs = self.processor(images=image_path, return_tensors="pt").to(self.device)
            
            # Generate caption
            with torch.no_grad():
                generated_ids = self.model.generate(
                    pixel_values=inputs.pixel_values,
                    max_length=512,  # Increase max length for more detailed descriptions
                    num_beams=10,    # Increase number of beams for better quality
                    repetition_penalty=1.2,  # Adjust repetition penalty
                    temperature=0.7,  # Adjust temperature for more deterministic output
                    top_p=0.85,      # Adjust top-p for more focused output
                    length_penalty=1.2,  # Increase length penalty for longer sequences
                    do_sample=True   # Use sampling instead of greedy decoding
                )
            
            # Decode the generated text
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return generated_text.strip()
        
        except Exception as e:
            print(f"Error generating description: {str(e)}")
            return "Error analyzing image. Please try again."