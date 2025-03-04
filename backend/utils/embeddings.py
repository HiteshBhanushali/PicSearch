import torch
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from config import Config

class EmbeddingModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingModel, cls).__new__(cls)
            cls._instance.model = None
        return cls._instance
    
    def load_model(self):
        """Load the Sentence-BERT model for generating embeddings"""
        if self.model is None:
            try:
                model_name = Config.SBERT_MODEL_NAME
                
                # Check if model exists locally
                local_path = f'./models/{model_name}'
                if os.path.exists(local_path):
                    self.model = SentenceTransformer(local_path)
                    print(f"Loaded SBERT model from local path: {local_path}")
                else:
                    print(f"Downloading SBERT model: {model_name}")
                    self.model = SentenceTransformer(model_name)
                    
                    # Save model locally for future use
                    os.makedirs(local_path, exist_ok=True)
                    self.model.save(local_path)
                    
                print("SBERT model loaded successfully")
            except Exception as e:
                print(f"Error loading SBERT model: {str(e)}")
                raise
    
    def get_embedding(self, texts):
        """Generate embeddings for the given texts"""
        if self.model is None:
            self.load_model()
        
        try:
            if isinstance(texts, list):
                return self.model.encode(texts, convert_to_numpy=True)
            else:
                return self.model.encode([texts], convert_to_numpy=True)[0]
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            raise
    
    def semantic_search(self, query, descriptions, top_k=10):
        """
        Perform semantic search to find images matching the query
        
        Args:
            query (str): The search query
            descriptions (list): List of dictionaries with image descriptions and their paths
            top_k (int): Number of top results to return
            
        Returns:
            list: List of matching image entries sorted by relevance
        """
        if self.model is None:
            self.load_model()
            
        try:
            # Generate embedding for the query
            query_embedding = self.get_embedding(query)
            
            # Get embeddings for all descriptions (or use cached ones)
            results = []
            
            for item in descriptions:
                description = item.get('description', '')
                
                # Get or generate embedding for this description
                if 'embedding' not in item or item['embedding'] is None:
                    item['embedding'] = self.get_embedding(description).tolist()
                
                # Convert embedding to numpy array if it's a list
                desc_embedding = np.array(item['embedding'])
                
                # Calculate cosine similarity
                similarity = self.cosine_similarity(query_embedding, desc_embedding)
                
                # Add to results if above threshold
                if similarity > 0.6:  # Minimum similarity threshold
                    results.append({
                        'image_path': item['image_path'],
                        'description': description,
                        'similarity': float(similarity)
                    })
            
            # Sort results by similarity (highest first)
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Return top-k results
            return results[:top_k]
            
        except Exception as e:
            print(f"Error in semantic search: {str(e)}")
            return []
    
    @staticmethod
    def cosine_similarity(a, b):
        """Calculate cosine similarity between two vectors"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))