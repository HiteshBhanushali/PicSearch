import React, { useState } from 'react';

const ImageCard = ({ image }) => {
  const [showFullDescription, setShowFullDescription] = useState(false);
  
  const toggleDescription = () => {
    setShowFullDescription(!showFullDescription);
  };
  
  const shortenDescription = (desc, maxLength = 150) => {
    if (desc.length <= maxLength) return desc;
    return desc.substring(0, maxLength) + '...';
  };
  
  return (
    <div className="image-card">
      <div className="image-container">
        <img 
          src={`http://localhost:5000/${image.image_path}`}
          alt={shortenDescription(image.description, 20)}
          className="card-image"
          loading="lazy"
        />
        {image.similarity !== undefined && (
          <div className="similarity-badge">
            {Math.round(image.similarity * 100)}% match
          </div>
        )}
      </div>
      {/* To add discription in Search images card as well. enable below code */}
      {/* <div className="card-content">
        <div className="description-container">
          <p className="image-description">
            {showFullDescription 
              ? image.description 
              : shortenDescription(image.description)}
          </p>
          
          {image.description.length > 150 && (
            <button 
              className="toggle-description" 
              onClick={toggleDescription}
            >
              {showFullDescription ? 'Show Less' : 'Show More'}
            </button>
          )}
        </div>
      </div> */}
    </div>
  );
};

export default ImageCard;