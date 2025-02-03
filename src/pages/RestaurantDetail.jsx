import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const RestaurantDetails = () => {
  const { id } = useParams(); 
  const [restaurant, setRestaurant] = useState(null); 
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null); 

  useEffect(() => {
    // Fetch restaurant details using the id
    const fetchRestaurantDetails = async () => {
      try {
        const response = await fetch(`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${id}`);
        const data = await response.json();

        if (data.meals) {
          setRestaurant(data.meals[0]); 
        } else {
          setError('Restaurant details not found');
        }
      } catch (err) {
        setError('Failed to fetch restaurant details');
      } finally {
        setLoading(false); 
      }
    };

    fetchRestaurantDetails(); 
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="restaurant-details">
      <h2>{restaurant.strMeal}</h2>
      <img src={restaurant.strMealThumb} alt={restaurant.strMeal} />
      <p>{restaurant.strInstructions}</p>
      <p><strong>Category:</strong> {restaurant.strCategory}</p>
      <p><strong>Cuisine:</strong> {restaurant.strArea}</p>
    </div>
  );
};

export default RestaurantDetails;
