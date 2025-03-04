import React from 'react';
import ImageUploader from '../components/ImageUploader';

const Upload = () => {
  return (
    <div className="upload-page">
      <div className="container">
        <div className="page-header">
          <h1>Upload & Analyze Images</h1>
          <p className="page-description">
            Upload one or more images to analyze. Each image will be processed by our AI
            to generate a detailed description capturing all visual elements.
          </p>
        </div>
        
        <ImageUploader />
        
        <div className="how-it-works">
          <h2>How It Works</h2>
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Upload</h3>
              <p>Select one or more images from your device</p>
            </div>
            
            <div className="step">
              <div className="step-number">2</div>
              <h3>Analyze</h3>
              <p>Our AI generates detailed descriptions of each image</p>
            </div>
            
            <div className="step">
              <div className="step-number">3</div>
              <h3>Search</h3>
              <p>Use the search feature to find images by content description</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;