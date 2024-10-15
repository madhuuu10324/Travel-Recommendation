import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // State for form inputs
  const [weather, setWeather] = useState('');
  const [destinationType, setDestinationType] = useState('');
  const [budget, setBudget] = useState('');
  const [userId, setUserId] = useState(''); // Optional if you decide to keep it

  // State for storing recommendations
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Reset error state

    // Validate form inputs
    if (!weather || !destinationType || !budget) { // Adjusted to remove userId check
      setError('Please fill in all fields.');
      return;
    }

    try {
      // Send the data to the backend API
      const response = await axios.post('http://localhost:8000/api/get-recommendations/', {
        weather,
        destination_type: destinationType,
        budget,
        user_id: userId // Remove this line if you don't want to send user_id
      });

      // Store the response data (recommendations)
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error.response ? error.response.data : error.message);
      setError('Failed to fetch recommendations. Please try again later.');
    }
  };

  return (
    <div className="app-container">
      <h1>Travel Recommendations</h1>

      {/* Error Message */}
      {error && <p className="error-message">{error}</p>}

      {/* Form for Input */}
      <form className="recommendation-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Preferred Weather</label>
          <select value={weather} onChange={(e) => setWeather(e.target.value)}>
            <option value="">Select Weather</option>
            <option value="hot">hot</option>
            <option value="cool">cool</option>
            <option value="moderate">moderate</option>
          </select>
        </div>

        <div className="form-group">
          <label>Destination Type</label>
          <select value={destinationType} onChange={(e) => setDestinationType(e.target.value)}>
            <option value="">Select Destination Type</option>
            <option value="Mountains">Mountains</option>
            <option value="City">City</option>
            <option value="Beach">Beach</option>
          </select>
        </div>

        <div className="form-group">
          <label>Budget (in INR)</label>
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            placeholder="Enter your budget"
          />
        </div>

        {/* Remove User ID input if not required */}
        <button type="submit">Get Recommendations</button>
      </form>

      {/* Display Recommendations */}
      <div className="recommendations-container">
        <h2>I would recommend...</h2>
        {recommendations.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <h3>{rec.destination}</h3>
            <p><strong>Weather:</strong> {rec.weather}</p>
            <p><strong>Destination Type:</strong> {rec.destination_type}</p>
            <p><strong>Itinerary:</strong> {rec.itinerary}</p>
            <p><strong>Places Covered:</strong> {rec.places_covered}</p>
            <p><strong>Hotel Details:</strong> {rec.hotel_details}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;