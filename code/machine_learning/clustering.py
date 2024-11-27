import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import DBSCAN
import numpy as np
import json

def cluster_users_with_state_label_encoding(profiles):
    """
    Cluster user profiles using DBSCAN with state features incorporated via label encoding.

    Args:
        profiles (pd.DataFrame): DataFrame with user profiles including
                                 'latitude', 'longitude', 'state', and 'money_spent'.

    Returns:
        pd.DataFrame: Original DataFrame with an additional 'cluster' column.
                      Users in cluster -1 are considered anomalies.
    """
    # Calculate total money spent over the past 12 years

    profiles['total_money_spent'] = profiles['money_spent'].apply(
        lambda x: sum(x.values())
    )

    # Encode state with label encoding
    label_encoder = LabelEncoder()
    profiles['state_encoded'] = label_encoder.fit_transform(profiles['state'])

    # Pull out money spent by year
    

    # Select features for clustering
    features = profiles[['lat', 'lng', 'state_encoded', 'total_money_spent']+\
                        [c for c in profiles.columns if c.startswith('money_spent_')]+
                        [c for c in profiles.columns if c.startswith('average_temperature_')]]

    # Standardize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=0.5, min_samples=10, metric='euclidean')
    clusters = dbscan.fit_predict(scaled_features)

    # Add cluster labels to the original DataFrame
    profiles['cluster'] = clusters

    return profiles

# Example usage
if __name__ == "__main__":

    # Read user profiles from a JSON file
    with open('synthetic_profiles.json', 'r') as file:
        profiles_data = json.load(file)

    # Convert to DataFrame
    profiles_df = pd.DataFrame(profiles_data)

    # Cluster the profiles
    clustered_profiles = cluster_users_with_state_label_encoding(profiles_df)

    # Save or display clustered profiles
    print(clustered_profiles[['name', 'id', 'state', 'cluster']])

    
