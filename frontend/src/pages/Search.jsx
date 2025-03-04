import React, { useState, useEffect } from 'react';
import SearchBar from '../components/SearchBar';
import ImageGrid from '../components/ImageGrid';
import apiService from '../services/api';

const Search = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [allImages, setAllImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    const fetchAllImages = async () => {
      try {
        const response = await apiService.getAllImages();
        setAllImages(response.images || []);
      } catch (err) {
        setError('Failed to load images');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchAllImages();
  }, []);
  
  const handleResultsChange = (results) => {
    setSearchResults(results);
    setHasSearched(true);
  };
  
  // Determine which images to show
  const displayImages = hasSearched ? searchResults : allImages;
  
  return (
    <div className="search-page">
      <div className="container">
        <div className="page-header">
          <h1>Search Images</h1>
          <p className="page-description">
            Search through your image collection using natural language. 
            The system uses semantic search to find images that match your description.
          </p>
        </div>
        
        <SearchBar onResultsChange={handleResultsChange} />
        
        {error && <p className="error-message">{error}</p>}
        
        <div className="search-results">
          <h2>
            {hasSearched 
              ? `Search Results (${searchResults.length})` 
              : `All Images (${allImages.length})`}
          </h2>
          
          <ImageGrid 
            images={displayImages} 
            loading={loading}
            emptyMessage={
              hasSearched 
                ? "No images match your search. Try a different query." 
                : "No images found. Upload some images to get started!"
            }
          />
        </div>
      </div>
    </div>
  );
};

export default Search;