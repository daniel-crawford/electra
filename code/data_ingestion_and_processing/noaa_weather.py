import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from tqdm import tqdm
import us

load_dotenv()

# NOAA API configuration
NOAA_API_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"


API_TOKEN = os.environ.get("NOAA_API_TOKEN")

# Define headers for the API request
HEADERS = {
    "token": API_TOKEN
}

STATE_FIPS = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}


# Function to fetch average temperature data for a specific state and year
def fetch_temperature_data(state, year):
    params = {
        "datasetid": "GHCND",  # Global Historical Climatology Network Daily
        "locationid": f"FIPS:{state}",  # FIPS code for US states
        "startdate": f"{year}-01-01",
        "enddate": f"{year}-12-31",
        "datatypeid": "TAVG",  # Average temperature
        "units": "metric",  # Metric (Celsius)
        "limit": 1000,  # Max number of records per request
    }

    response = requests.get(NOAA_API_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error fetching data for {state} in {year}: {response.text}")
        return []

# Function to process data and calculate monthly averages
def calculate_monthly_averages(state, years):
    monthly_averages = []
    for year in years:
        data = fetch_temperature_data(state, year)
        if data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Convert temperature values

            monthly_avg = df.groupby('month')['value'].mean().reset_index()
            monthly_avg['state'] = state
            monthly_avg['year'] = year

            monthly_averages.append(monthly_avg)

    # Combine all years into a single DataFrame
    return pd.concat(monthly_averages, ignore_index=True) if monthly_averages else pd.DataFrame()

# Main function to get temperature data for all states
def get_temperature_data_for_all_states(output_file):
    # Define state FIPS codes and years since 2010
    state_fips = ["01", "02"]
    state_fips = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19", 
                  "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", 
                  "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", 
                  "54", "55", "56"]  # All state FIPS codes
                  

    years = range(2010, datetime.now().year + 1)

    all_data = []
    for state in tqdm(state_fips, desc="Fetching data for states"):
        print(f"Fetching data for state: {state}")
        state_data = calculate_monthly_averages(state, years)
        if not state_data.empty:
            all_data.append(state_data)

    # Combine all state data
    combined_data = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

    combined_data['state'] = combined_data['state'].apply(lambda x: us.states.lookup(x).name)

    # Save to CSV
    combined_data.to_csv(output_file, index=False)
    print("Data saved to average_monthly_temperatures.csv")

# Run the script
if __name__ == "__main__":
    get_temperature_data_for_all_states("data/NOAA_state_average_monthly_temperatures.csv")
