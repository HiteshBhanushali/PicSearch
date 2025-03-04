import React, { useState, useEffect, useRef } from 'react';
import apiService from '../services/api';

const SearchBar = ({ onResultsChange }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const searchTimeout = useRef(null);
  
  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) {
      onResultsChange([]);
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await apiService.searchImages(searchQuery);
      onResultsChange(response.results || []);
    } catch (err) {
      setError('Search failed. Please try again.');
      console.error(err);
      onResultsChange([]);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    // Clear previous timeout
    if (searchTimeout.current) {
      clearTimeout(searchTimeout.current);
    }
    
    // Debounce search to avoid excessive API calls
    searchTimeout.current = setTimeout(() => {
      handleSearch(query);
    }, 500);
    
    return () => {
      if (searchTimeout.current) {
        clearTimeout(searchTimeout.current);
      }
    };
  }, [query]);
  
  return (
    <div className="search-bar">
      <h2>Search Images</h2>
      <div className="search-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe what you're looking for..."
          className="search-input"
        />
        {loading && <span className="loading-indicator">Searching...</span>}
      </div>
      
      {error && <p className="error-message">{error}</p>}
      
      <p className="search-instructions">
        Type your search query above to find relevant images. The system will match your query with image descriptions.
      </p>
    </div>
  );
};

export default SearchBar;