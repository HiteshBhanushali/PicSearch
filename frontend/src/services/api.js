import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiService = {
  // Upload images
  uploadImages: async (imageFiles) => {
    const formData = new FormData();
    
    imageFiles.forEach(file => {
      formData.append('images', file);
    });
    
    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error uploading images:', error);
      throw error;
    }
  },
  
  // Search images
  searchImages: async (query) => {
    try {
      const response = await axios.get(`${API_URL}/search`, {
        params: { query }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error searching images:', error);
      throw error;
    }
  },
  
  // Get all images
  getAllImages: async () => {
    try {
      const response = await axios.get(`${API_URL}/all_images`);
      return response.data;
    } catch (error) {
      console.error('Error fetching all images:', error);
      throw error;
    }
  }
};

export default apiService;