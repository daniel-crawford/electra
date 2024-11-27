import json
import os
import pandas as pd
import sys


sys.path.append("./code/")
from data_ingestion_and_processing.data_ingestion import load_energy_data, clean_data
from data_ingestion_and_processing.customer_generation import generate_synthetic_profiles
from machine_learning.clustering import cluster_users_with_state_label_encoding
from machine_learning.classification import identify_high_spenders
from machine_learning.roi_prediction import predict_roi_with_clusters

ENERGY_DATA = "data/EIA_sales_revenue.csv"
TEMPERATURE_DATA = "data/average_monthly_temperature_by_state_2010-2022.csv"
CUSTOMER_DATA = "synthetic_profiles.json"



# Load datasets from different sources
energy_data = load_energy_data(ENERGY_DATA, "csv")
temperature_data = load_energy_data(TEMPERATURE_DATA, "csv")

# Clean, save, combine individual datasets
energy_data = clean_data(energy_data)
full_data = pd.merge(energy_data, temperature_data, on=['year','month','state'], how='inner')
full_data.to_csv("full_data.csv", index=False)

# Generate profiles
synthetic_profiles = generate_synthetic_profiles(full_data, num_profiles=1000)

# Save the profiles to a JSON file
output_path = CUSTOMER_DATA 
with open(output_path, "w") as f:
    json.dump(synthetic_profiles, f, indent=4)

# Convert to DataFrame
profiles_df = pd.DataFrame(synthetic_profiles)

# Cluster the profiles
clustered_profiles = cluster_users_with_state_label_encoding(profiles_df)

# Identify high spenders
result = identify_high_spenders(clustered_profiles, threshold=1.5)

# Predict ROI
profiles_with_roi = predict_roi_with_clusters(result)



