from flask import Flask, jsonify, request
import pandas as pd
import sys
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


sys.path.append("./code/")
from data_ingestion_and_processing.data_ingestion import load_energy_data, clean_data
from data_ingestion_and_processing.customer_generation import generate_synthetic_profiles
from machine_learning.clustering import cluster_users_with_state_label_encoding
from machine_learning.classification import identify_high_spenders
from machine_learning.roi_prediction import predict_roi_with_clusters

ENERGY_DATA = "data/EIA_sales_revenue.csv"
TEMPERATURE_DATA = "data/average_monthly_temperature_by_state_2010-2022.csv"
CUSTOMER_DATA = "synthetic_profiles.json"

# Load synthetic customer data
with open(CUSTOMER_DATA, 'r') as f:
    synthetic_profiles = json.load(f)

# Load datasets from different sources
energy_data = load_energy_data(ENERGY_DATA, "csv")
temperature_data = load_energy_data(TEMPERATURE_DATA, "csv")

# Clean, save, combine individual datasets
energy_data = clean_data(energy_data)
full_data = pd.merge(energy_data, temperature_data, on=['year','month','state'], how='inner')
full_data.to_csv("full_data.csv", index=False)

# Generate synthetic customer data
def generate_customers():
    profiles_df = pd.DataFrame(synthetic_profiles)
    return profiles_df

# Perform clustering
def cluster_customers(customers, sensativity = 1):
    print('Clustering customers..')
    clustered_profiles = cluster_users_with_state_label_encoding(customers)
    result = identify_high_spenders(clustered_profiles, threshold=1.5/sensativity)
    profiles_with_roi = predict_roi_with_clusters(result)


    profiles_with_roi['spender_class'] = profiles_with_roi[['spender_class','predicted_roi']]\
        .apply(lambda x: 
                'HIGH ROI' if x['predicted_roi'] > 1.5
                else 'High Spender' if x['spender_class'] == 'high'
                else 'Normal', axis = 1)
    return profiles_with_roi

# Endpoint to get clustered data
@app.route('/api/customers', methods=['GET'])
def get_customers():
    #sensativity = float(request.args.get('sensativity', 10))  # Get the eps parameter from the query string
    customers = generate_customers()
    profiles_with_roi = cluster_customers(customers)
    return jsonify(profiles_with_roi.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
