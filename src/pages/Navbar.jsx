import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ searchQuery, setSearchQuery, token, handleLogout }) => {
  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <input
        type="text"
        placeholder="Search restaurants..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      {token ? (
        <>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </>
      )}
    </nav>
  );
};

export default Navbar;
