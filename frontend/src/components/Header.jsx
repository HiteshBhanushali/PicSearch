import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <h1 className="logo">PicSearch</h1>
        <nav className="nav">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/upload">Upload Images</Link>
            </li>
            <li>
              <Link to="/search">Search Images</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;