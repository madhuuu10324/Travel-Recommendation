# Travel Recommendation System

Welcome to the Travel Recommendation System! This project provides personalized travel recommendations based on user preferences such as weather, destination type, and budget. It leverages both content-based and collaborative filtering methods to deliver tailored suggestions.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Features
- **Personalized Recommendations**: Users can receive travel suggestions based on their preferences.
- **Content-Based Filtering**: Filters destinations based on user-specified criteria like weather and destination type.
- **Collaborative Filtering**: Utilizes user ratings to find similar users and recommend destinations they enjoyed.
- **Accuracy Metrics**: Provides feedback on the quality of recommendations.

## Technology Stack
- **Frontend**: ReactJS
- **Backend**: Django, Django REST Framework
- **Data Processing**: Pandas, Scikit-learn
- **Database**: SQLite (or any database you configure)
- **Other**: Virtualenv for Python environment management

## Installation

### Frontend
Navigate to the `travel-recommendation-app` folder and install the required Node modules:

```bash
cd travel-recommendation-app
npm install
```
### Backend
Navigate to the `travel_recommendation` folder and set up your virtual environment:
```bash
cd travel_recommendation
mkvirtualenv <env_name>
workon <env_name>
pip install -r requirements.txt
python manage.py runserver
```
## Usage
Once both the frontend and backend servers are running, navigate to the frontend application in your browser. The frontend will interact with the backend to fetch travel recommendations based on user input.
### Frontend Interaction
- Enter your preferences (weather, destination type, budget).
- Submit the form to receive personalized travel recommendations.
- View recommendations displayed on the screen.

## API Endpoints
The backend exposes the following API endpoint:

- **POST** `/api/get_recommendations/`
  - **Request Body**:
    ```json
    {
      "weather": "string",
      "destination_type": "string",
      "budget": "float",
      "user_id": "int"
    }
    ```
  - **Response**:
    ```json
    {
      "recommendations": [
        {
          "destination": "string",
          "weather": "string",
          "itinerary": "string",
          "destination_type": "string",
          "places_covered": "string",
          "hotel_details": "string"
        }
      ],
      "accuracy": {
        "hits": "int",
        "precision": "float",
        "recall": "float",
        "f1_score": "float"
      }
    }
    ```

