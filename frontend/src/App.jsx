import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Search from './pages/Search';
import './styles.css';

const App = () => {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/search" element={<Search />} />
          </Routes>
        </main>
        <div className="social-media-links">
          <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
          <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer">Twitter</a>
          <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">Instagram</a>
          <a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </div>
        <footer className="footer">
          <div className="container">
            <p>&copy; {new Date().getFullYear()} PicSearch App</p>
            <p>
              <a href="/privacy-policy">Privacy Policy</a> | 
              <a href="/terms-of-service">Terms of Service</a> | 
              <a href="/contact">Contact Us</a>
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
};

export default App;