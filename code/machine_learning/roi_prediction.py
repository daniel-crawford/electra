import pandas as pd
import numpy as np
from sklearn.metrics import euclidean_distances
import json


def predict_roi_with_clusters(clustered_profiles):
    """
    Predict ROI for profiles as a return to the center of the cluster.

    Args:
        clustered_profiles (pd.DataFrame): DataFrame with clustered profiles, including
                                           'latitude', 'longitude', 'total_money_spent',
                                           'average_temperature', and 'cluster'.

    Returns:
        pd.DataFrame: Updated DataFrame with an additional 'predicted_roi' column.
    """
    clustered_profiles.groupby('cluster')['total_money_spent'].agg(['mean', 'std']).reset_index()

    clustered_profiles['predicted_roi'] = 1-(clustered_profiles['cluster_avg'] - clustered_profiles['total_money_spent'])/clustered_profiles['total_money_spent']
    return clustered_profiles

# Example usage
if __name__ == "__main__":
    from clustering import cluster_users_with_state_label_encoding
    from classification import identify_high_spenders

    # Read user profiles from a JSON file
    with open('synthetic_profiles.json', 'r') as file:
        profiles_data = json.load(file)

    # Convert to DataFrame
    profiles_df = pd.DataFrame(profiles_data)

    # Cluster the profiles
    clustered_profiles = cluster_users_with_state_label_encoding(profiles_df)

    # Identify high spenders
    result = identify_high_spenders(clustered_profiles, threshold=1.5)

    # Predict ROI
    profiles_with_roi = predict_roi_with_clusters(result)

 
    # Display results
    print(profiles_with_roi[['name', 'id', 'state', 'cluster', 'predicted_roi']])

    print(profiles_with_roi['predicted_roi'].describe())

    print(profiles_with_roi[profiles_with_roi['spender_class']=='high']['predicted_roi'].describe())
