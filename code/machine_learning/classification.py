import pandas as pd
import numpy as np
import json
import sys 

#from clustering import cluster_users_with_state_label_encoding

def identify_high_spenders(clustered_profiles, threshold=1.5):
    """
    Identify profiles paying more than their peers in each cluster.

    Args:
        clustered_profiles (pd.DataFrame): DataFrame with clustered profiles, including 'cluster' and 'total_money_spent'.
        threshold (float): Multiplier for determining "high spender" (default: 1.5x the cluster average).

    Returns:
        pd.DataFrame: DataFrame with an additional 'spender_class' column:
                      - 'normal': Normal spenders within the cluster.
                      - 'high': High spenders within the cluster.
    """
    # Calculate the average and standard deviation of spending for each cluster
    cluster_stats = clustered_profiles.groupby('cluster')['total_money_spent'].agg(['mean', 'std']).reset_index()
    cluster_stats.rename(columns={'mean': 'cluster_avg', 'std': 'cluster_std'}, inplace=True)

    # Merge cluster statistics back into the original DataFrame
    clustered_profiles = clustered_profiles.merge(cluster_stats, on='cluster', how='left')

    # Classify profiles based on spending relative to their cluster average
    clustered_profiles['spender_class'] = clustered_profiles.apply(
        lambda row: 'high' if row['total_money_spent'] > row['cluster_avg'] * threshold else 'normal',
        axis=1
    )

    return clustered_profiles

# Example usage
if __name__ == "__main__":
    
    # Read user profiles from a JSON file
    with open('synthetic_profiles.json', 'r') as file:
        profiles_data = json.load(file)

    # Convert to DataFrame
    profiles_df = pd.DataFrame(profiles_data)

    # Cluster the profiles
    clustered_profiles = cluster_users_with_state_label_encoding(profiles_df)

    # Identify high spenders
    result = identify_high_spenders(profiles_df, threshold=1.5)

    # Display results
    print(result[['name', 'id', 'state', 'cluster', 'total_money_spent', 'spender_class']])

    print(result['cluster'].value_counts())

    print(result['spender_class'].value_counts())
