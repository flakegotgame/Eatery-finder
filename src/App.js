import React, { useState, useEffect } from 'react';
import { Route, Routes, Link } from 'react-router-dom';
import './App.css'; 
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RestaurantDetails from './pages/RestaurantDetail';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    if (token) {
      fetchRestaurants();
    }
  }, [token]);

  const fetchRestaurants = () => {
    fetch('https://www.themealdb.com/api/json/v1/1/search.php?s=') 
      .then((response) => response.json())
      .then((data) => {
        if (data && data.meals && Array.isArray(data.meals)) {
          setRestaurants(data.meals);
        } else {
          setRestaurants([]);
        }
      })
      .catch((error) => console.error('Error fetching restaurants:', error));
  };

  return (
    <div className="App">
      <nav className="navbar">
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
        {token && <Link to="/restaurants">Search Restaurant</Link>}
      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage setToken={setToken} />} />
        <Route
          path="/restaurants"
          element={<RestaurantList restaurants={restaurants} />}
        />
        <Route
          path="/restaurants/:id"
          element={<RestaurantDetails />}
        />
      </Routes>
    </div>
  );
};

const RestaurantList = ({ restaurants }) => (
  <div className="restaurant-list">
    {restaurants.length ? (
      restaurants.map((restaurant) => (
        <div className="restaurant-card" key={restaurant.idMeal}>
          <img
            src={restaurant.strMealThumb || "https://via.placeholder.com/200"}
            alt={restaurant.strMeal}
            className="restaurant-img"
          />
          <h3>{restaurant.strMeal}</h3>
          <p>{restaurant.strArea}</p>
          <Link to={`/restaurants/${restaurant.idMeal}`} className="details-link">
            More Info
          </Link>
        </div>
      ))
    ) : (
      <p>No restaurants available</p>
    )}
  </div>
);

export default App;
