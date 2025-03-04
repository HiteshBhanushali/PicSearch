import React from 'react';
import ImageCard from './ImageCard';

const ImageGrid = ({ images, loading, emptyMessage }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <p>Loading images...</p>
      </div>
    );
  }
  
  if (!images || images.length === 0) {
    return (
      <div className="empty-state">
        <p>{emptyMessage || 'No images found'}</p>
      </div>
    );
  }
  
  return (
    <div className="image-grid">
      {images.map((image, index) => (
        <ImageCard key={image.id || index} image={image} />
      ))}
    </div>
  );
};

export default ImageGrid;