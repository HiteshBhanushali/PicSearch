import React, { useState } from 'react';
import apiService from '../services/api';

const ImageUploader = () => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (files.length === 0) {
      setError('Please select at least one image to upload');
      return;
    }

    setUploading(true);
    setShowModal(true);
    setStatusMessage('Analyzing images...');
    setError('');

    try {
      const response = await apiService.uploadImages(files);
      setResults(response.results);
      setFiles([]);
      setStatusMessage('Analysis complete!');
    } catch (err) {
      setError('Failed to upload images. Please try again.');
      console.error(err);
      setStatusMessage('Failed to analyze images.');
    } finally {
      setUploading(false);
      setTimeout(() => setShowModal(false), 2000); // Close modal after 2 seconds
    }
  };

  return (
    <div className="image-uploader">
      <h2>Upload Images for Analysis</h2>

      <form onSubmit={handleUpload}>
        <div className="file-input-container">
          <input
            type="file"
            accept="image/*"
            multiple
            onChange={handleFileChange}
            disabled={uploading}
          />
          <p className="file-info">
            {files.length > 0 
              ? `Selected ${files.length} file${files.length > 1 ? 's' : ''}`
              : 'Select one or more images to analyze'}
          </p>
        </div>

        {error && <p className="error-message">{error}</p>}

        <button 
          type="submit" 
          className="upload-button"
          disabled={uploading || files.length === 0}
        >
          {uploading ? 'Analyzing...' : 'Upload and Analyze'}
        </button>
      </form>

      {results.length > 0 && (
        <div className="results-container">
          <h3>Analysis Results</h3>

          <div className="results-grid">
            {results.map((result, index) => (
              <div key={index} className="result-card">
                {result.success ? (
                  <>
                    <img 
                      src={`http://localhost:5000/${result.image_path}`}
                      alt={`Uploaded ${index}`}
                      className="result-image"
                    />
                    <div className="result-description">
                      <h4>Generated Description:</h4>
                      <p>{result.description}</p>
                    </div>
                  </>
                ) : (
                  <div className="error-card">
                    <p>Failed to process image</p>
                    {result.error && <p className="error-details">{result.error}</p>}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {showModal && (
        <div className="modal" style={{ display: 'block' }}>
          <div className="modal-content">
            <div className="spinner"></div>
            <p>{statusMessage}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;