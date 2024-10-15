import os
import pandas as pd
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity

@api_view(['POST'])
def get_recommendations(request):
    # User preferences from the frontend
    weather = request.data.get('weather')
    destination_type = request.data.get('destination_type')
    budget = request.data.get('budget')
    user_id = request.data.get('user_id')

    print(f"Received request with: weather={weather}, destination_type={destination_type}, budget={budget}, user_id={user_id}")

    # Validate budget input
    if budget is None:
        return Response({'error': 'Budget is required.'}, status=400)
    try:
        budget = float(budget)
    except ValueError:
        return Response({'error': 'Budget must be a valid number.'}, status=400)

    # Load the CSV data
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'filtered_semidata_cleaned_with_weather.csv')
    df = pd.read_csv(csv_file_path)

    # Step 1: Content-Based Filtering
    filtered = df[(df['weather'] == weather) & (df['destination_type'] == destination_type)]
    filtered['cost_per_person'] = pd.to_numeric(filtered['cost_per_person'], errors='coerce')
    filtered = filtered[filtered['cost_per_person'] <= budget]

    if filtered.empty:
        print("No matching destinations found after content-based filtering.")
        return Response({'recommendations': []})

    # Step 2: Collaborative Filtering
    ratings_file_path = os.path.join(settings.BASE_DIR, 'data', 'user_ratings.csv')
    user_ratings_df = pd.read_csv(ratings_file_path)
    ratings_pivot = user_ratings_df.pivot_table(index='user_id', columns='destination', values='rating').fillna(0)

    # Cosine similarity
    user_similarity = cosine_similarity(ratings_pivot)
    user_similarity_df = pd.DataFrame(user_similarity, index=ratings_pivot.index, columns=ratings_pivot.index)

    if user_id in user_similarity_df.index:
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).index
        print(f"Similar users found: {similar_users.tolist()}")
    else:
        print(f"No similar users found for user_id={user_id}")
        similar_users = []

    collaborative_recommendations = set()
    for similar_user in similar_users:
        similar_user_ratings = ratings_pivot.loc[similar_user]
        top_rated_destinations = similar_user_ratings[similar_user_ratings > 0].index.tolist()
        collaborative_recommendations.update(top_rated_destinations)

    print(f"Collaborative recommendations: {collaborative_recommendations}")

    # Combine recommendations
    recommended_destinations = filtered[filtered['destination'].isin(collaborative_recommendations)]

    if recommended_destinations.empty:
        recommended_destinations = filtered

    unique_destinations = set()
    result = []

    for _, row in recommended_destinations.iterrows():
        if row['destination'] not in unique_destinations:
            unique_destinations.add(row['destination'])
            result.append({
                "destination": row['destination'],
                "weather": row['weather'],
                "itinerary": row['itinerary'],
                "destination_type": row['destination_type'],
                "places_covered": row['places_covered'],
                "hotel_details": row['hotel_details']
            })

        if len(result) >= 5:
            break

    # Calculate accuracy metrics (you'll need to define get_relevant_items_for_user)
    relevant_items = get_relevant_items_for_user(user_id)  # Implement this function
    accuracy_metrics = calculate_accuracy([item["destination"] for item in result], relevant_items)

    print(f"Accuracy Metrics: {accuracy_metrics}")

    return Response({"recommendations": result, "accuracy": accuracy_metrics})

def calculate_accuracy(recommended_items, relevant_items):
    recommended_set = set(recommended_items)
    relevant_set = set(relevant_items)

    hits = recommended_set.intersection(relevant_set)

    precision = len(hits) / len(recommended_set) if recommended_set else 0
    recall = len(hits) / len(relevant_set) if relevant_set else 0
    f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    return {
        "hits": len(hits),
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
    }

def get_relevant_items_for_user(user_id):
    # You need to implement this function based on your logic to retrieve relevant items
    # For example, it could be based on user ratings or previous interactions
    return ["Dharamshala", "Goa"]  # Example return, replace with actual logic