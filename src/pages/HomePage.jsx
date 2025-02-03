import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css'; 

const HomePage = () => {
  return (
    <div className="home-page">
      <h2>Welcome to the Restaurant Finder</h2>
      <p>Select a restaurant from the list to view more details.</p>
      <Link to="/restaurants">
        <button className="view-restaurants-button">View Restaurants</button>
      </Link>
    </div>
  );
};

export default HomePage;
