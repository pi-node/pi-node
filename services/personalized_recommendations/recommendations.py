import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load user data
user_data = pd.read_csv('user_data.csv')

# Load service data
service_data = pd.read_csv('service_data.csv')

# Merge user and service data
merged_data = pd.merge(user_data, service_data, on='service_id')

# Create user-service matrix
user_service_matrix = merged_data.pivot_table(index='user_id', columns='service_id', values='rating')

# Calculate similarity between users
user_similarity = cosine_similarity(user_service_matrix)

# Function to generate recommendations for a user
def generate_recommendations(user_id, top_n=5):
    # Get index of the user
    user_index = user_service_matrix.index.get_loc(user_id)

    # Get similarity scores for the user
    similarity_scores = user_similarity[user_index]

    # Get top N similar users
    top_similar_users = similarity_scores.argsort()[:-(top_n + 1):-1]

    # Get recommended services for the user
    recommended_services = []
    for similar_user in top_similar_users:
        recommended_services.extend(user_service_matrix.iloc[similar_user].index)

    # Return recommended services
    return recommended_services
