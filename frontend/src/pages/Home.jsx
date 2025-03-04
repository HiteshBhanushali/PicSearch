import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ImageGrid from '../components/ImageGrid';
import apiService from '../services/api';

const Home = () => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await apiService.getAllImages();
        setImages(response.images || []);
      } catch (err) {
        setError('Failed to load images');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchImages();
  }, []);
  
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>AI-Powered Image Analysis & Search</h1>
        <p className="subtitle">
          Upload images to generate detailed descriptions, then search across your collection
          using natural language queries.
        </p>
        
        <div className="cta-buttons">
          <Link to="/upload" className="cta-button primary">
            Upload Images
          </Link>
          <Link to="/search" className="cta-button secondary">
            Search Collection
          </Link>
        </div>
      </div>
      
      {error && <p className="error-message">{error}</p>}
      
      <div className="recent-images">
        <h2>Recent Images</h2>
        <ImageGrid 
          images={images.slice(0, 8)} 
          loading={loading}
          emptyMessage="No images in collection. Upload some images to get started!"
        />
        
        {images.length > 8 && (
          <div className="view-all">
            <Link to="/search" className="view-all-link">
              View All Images
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;