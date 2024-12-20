import pandas as pd
import random
import json
import numpy as np
from tqdm import tqdm

# Load your dataset
file_path = 'full_data.csv'  # Replace with your dataset file path
data = pd.read_csv(file_path)

STATE_STDs = {
    #std of average usage
    state: np.std(data[data['state'] == state]['megawatthours']/data[data['state'] == state]['customers']) for state in data['state'].unique()
}



STATE_BOUNDS = {
  "AK":
  {
    "name": "Alaska",
    "min_lat": 52.5964,
    "max_lat": 71.5232,
    "min_lng": -169.9146,
    "max_lng": -129.993
  },
  "AL":
  {
    "name": "Alabama",
    "min_lat": 30.1463,
    "max_lat": 35.0041,
    "min_lng": -88.4743,
    "max_lng": -84.8927
  },
  "AR":
  {
    "name": "Arkansas",
    "min_lat": 33.0075,
    "max_lat": 36.4997,
    "min_lng": -94.6198,
    "max_lng": -89.6594
  },
  "AZ":
  {
    "name": "Arizona",
    "min_lat": 31.3325,
    "max_lat": 37.0004,
    "min_lng": -114.8126,
    "max_lng": -109.0475
  },
  "CA":
  {
    "name": "California",
    "min_lat": 32.5121,
    "max_lat": 42.0126,
    "min_lng": -124.6509,
    "max_lng": -114.1315
  },
  "CO":
  {
    "name": "Colorado",
    "min_lat": 36.9949,
    "max_lat": 41.0006,
    "min_lng": -109.0489,
    "max_lng": -102.0424
  },
  "CT":
  {
    "name": "Connecticut",
    "min_lat": 40.9509,
    "max_lat": 42.0511,
    "min_lng": -73.7272,
    "max_lng": -71.7874
  },
  "DE":
  {
    "name": "Delaware",
    "min_lat": 38.4482,
    "max_lat": 39.8296,
    "min_lng": -75.7919,
    "max_lng": -74.8526
  },
  "FL":
  {
    "name": "Florida",
    "min_lat": 24.3959,
    "max_lat": 31.0035,
    "min_lng": -87.6256,
    "max_lng": -79.8198
  },
  "GA":
  {
    "name": "Georgia",
    "min_lat": 30.3575,
    "max_lat": 34.9996,
    "min_lng": -85.6082,
    "max_lng": -80.696
  },
  "HI":
  {
    "name": "Hawaii",
    "min_lat": 18.71,
    "max_lat": 22.3386,
    "min_lng": -160.3922,
    "max_lng": -154.6271
  },
  "IA":
  {
    "name": "Iowa",
    "min_lat": 40.3622,
    "max_lat": 43.5008,
    "min_lng": -96.6357,
    "max_lng": -90.1538
  },
  "ID":
  {
    "name": "Idaho",
    "min_lat": 41.9871,
    "max_lat": 49.0018,
    "min_lng": -117.2372,
    "max_lng": -111.0471
  },
  "IL":
  {
    "name": "Illinois",
    "min_lat": 36.9894,
    "max_lat": 42.5116,
    "min_lng": -91.512,
    "max_lng": -87.0213
  },
  "IN":
  {
    "name": "Indiana",
    "min_lat": 37.7718,
    "max_lat": 41.7611,
    "min_lng": -88.098,
    "max_lng": -84.809
  },
  "KS":
  {
    "name": "Kansas",
    "min_lat": 36.9927,
    "max_lat": 40.0087,
    "min_lng": -102.0506,
    "max_lng": -94.6046
  },
  "KY":
  {
    "name": "Kentucky",
    "min_lat": 36.4931,
    "max_lat": 39.1439,
    "min_lng": -89.5372,
    "max_lng": -82.0308
  },
  "LA":
  {
    "name": "Louisiana",
    "min_lat": 28.8832,
    "max_lat": 33.0225,
    "min_lng": -94.043,
    "max_lng": -88.7421
  },
  "MA":
  {
    "name": "Massachusetts",
    "min_lat": 41.159,
    "max_lat": 42.889,
    "min_lng": -73.5081,
    "max_lng": -69.7398
  },
  "MD":
  {
    "name": "Maryland",
    "min_lat": 37.8889,
    "max_lat": 39.722,
    "min_lng": -79.4861,
    "max_lng": -74.8581
  },
  "ME":
  {
    "name": "Maine",
    "min_lat": 42.9182,
    "max_lat": 47.455,
    "min_lng": -71.0829,
    "max_lng": -66.8628
  },
  "MI":
  {
    "name": "Michigan",
    "min_lat": 41.6965,
    "max_lat": 48.3042,
    "min_lng": -90.4175,
    "max_lng": -82.1221
  },
  "MN":
  {
    "name": "Minnesota",
    "min_lat": 43.5008,
    "max_lat": 49.3877,
    "min_lng": -97.2304,
    "max_lng": -89.4919
  },
  "MO":
  {
    "name": "Missouri",
    "min_lat": 35.9958,
    "max_lat": 40.6181,
    "min_lng": -95.7527,
    "max_lng": -89.1005
  },
  "MS":
  {
    "name": "Mississippi",
    "min_lat": 30.0905,
    "max_lat": 35.0075,
    "min_lng": -91.6589,
    "max_lng": -88.0994
  },
  "MT":
  {
    "name": "Montana",
    "min_lat": 44.3563,
    "max_lat": 48.9991,
    "min_lng": -116.0458,
    "max_lng": -104.0186
  },
  "NC":
  {
    "name": "North Carolina",
    "min_lat": 33.7666,
    "max_lat": 36.588,
    "min_lng": -84.3201,
    "max_lng": -75.4129
  },
  "ND":
  {
    "name": "North Dakota",
    "min_lat": 45.934,
    "max_lat": 48.9982,
    "min_lng": -104.0501,
    "max_lng": -96.5671
  },
  "NE":
  {
    "name": "Nebraska",
    "min_lat": 39.9992,
    "max_lat": 43.0006,
    "min_lng": -104.0543,
    "max_lng": -95.3091
  },
  "NH":
  {
    "name": "New Hampshire",
    "min_lat": 42.6986,
    "max_lat": 45.3058,
    "min_lng": -72.5592,
    "max_lng": -70.5583
  },
  "NJ":
  {
    "name": "New Jersey",
    "min_lat": 38.8472,
    "max_lat": 41.3593,
    "min_lng": -75.5708,
    "max_lng": -73.8885
  },
  "NM":
  {
    "name": "New Mexico",
    "min_lat": 31.3337,
    "max_lat": 36.9982,
    "min_lng": -109.0489,
    "max_lng": -103.0023
  },
  "NV":
  {
    "name": "Nevada",
    "min_lat": 35.003,
    "max_lat": 42.0003,
    "min_lng": -120.0037,
    "max_lng": -114.0436
  },
  "NY":
  {
    "name": "New York",
    "min_lat": 40.4772,
    "max_lat": 45.0153,
    "min_lng": -79.7624,
    "max_lng": -71.7517
  },
  "OH":
  {
    "name": "Ohio",
    "min_lat": 38.3761,
    "max_lat": 42.321,
    "min_lng": -84.8172,
    "max_lng": -80.5188
  },
  "OK":
  {
    "name": "Oklahoma",
    "min_lat": 33.6386,
    "max_lat": 37.0015,
    "min_lng": -103.0064,
    "max_lng": -94.4357
  },
  "OR":
  {
    "name": "Oregon",
    "min_lat": 41.9952,
    "max_lat": 46.2891,
    "min_lng": -124.7305,
    "max_lng": -116.4606
  },
  "PA":
  {
    "name": "Pennsylvania",
    "min_lat": 39.7199,
    "max_lat": 42.5167,
    "min_lng": -80.5243,
    "max_lng": -74.707
  },
  "RI":
  {
    "name": "Rhode Island",
    "min_lat": 41.1849,
    "max_lat": 42.0156,
    "min_lng": -71.9041,
    "max_lng": -71.0541
  },
  "SC":
  {
    "name": "South Carolina",
    "min_lat": 32.0453,
    "max_lat": 35.2075,
    "min_lng": -83.3588,
    "max_lng": -78.4836
  },
  "SD":
  {
    "name": "South Dakota",
    "min_lat": 42.4772,
    "max_lat": 45.9435,
    "min_lng": -104.0529,
    "max_lng": -96.438
  },
  "TN":
  {
    "name": "Tennessee",
    "min_lat": 34.9884,
    "max_lat": 36.6871,
    "min_lng": -90.3131,
    "max_lng": -81.6518
  },
  "TX":
  {
    "name": "Texas",
    "min_lat": 25.8419,
    "max_lat": 36.5008,
    "min_lng": -106.6168,
    "max_lng": -93.5074
  },
  "UT":
  {
    "name": "Utah",
    "min_lat": 36.9982,
    "max_lat": 41.9993,
    "min_lng": -114.0504,
    "max_lng": -109.0462
  },
  "VA":
  {
    "name": "Virginia",
    "min_lat": 36.5427,
    "max_lat": 39.4659,
    "min_lng": -83.6753,
    "max_lng": -74.9707
  },
  "VT":
  {
    "name": "Vermont",
    "min_lat": 42.7289,
    "max_lat": 45.0153,
    "min_lng": -73.4381,
    "max_lng": -71.4949
  },
  "WA":
  {
    "name": "Washington",
    "min_lat": 45.5439,
    "max_lat": 49.0027,
    "min_lng": -124.8679,
    "max_lng": -116.9165
  },
  "WI":
  {
    "name": "Wisconsin",
    "min_lat": 42.4954,
    "max_lat": 47.31,
    "min_lng": -92.8564,
    "max_lng": -86.2523
  },
  "WV":
  {
    "name": "West Virginia",
    "min_lat": 37.1953,
    "max_lat": 40.6338,
    "min_lng": -82.6392,
    "max_lng": -77.731
  },
  "WY":
  {
    "name": "Wyoming",
    "min_lat": 40.9986,
    "max_lat": 44.9998,
    "min_lng": -111.0539,
    "max_lng": -104.0556
  },
  "AS":
  {
    "name": "American Samoa",
    "min_lat": -14.377579,
    "max_lat": -14.221549,
    "min_lng": -170.851479,
    "max_lng": -170.539742
  },
  "DC":
  {
    "name": "District of Columbia",
    "min_lat": 38.79164435,
    "max_lat": 39.031386,
    "min_lng": -77.11979522,
    "max_lng": -76.867218
  },
  "FM":
  {
    "name": "Federated States of Micronesia",
    "min_lat": 6.673985,
    "max_lat": 7.202918,
    "min_lng": 157.651062,
    "max_lng": 158.595886
  },
  "GU":
  {
    "name": "Guam",
    "min_lat": 13.227058,
    "max_lat": 14.204108,
    "min_lng": 144.598961,
    "max_lng": 145.301743
  },
  "MH":
  {
    "name": "Marshall Islands",
    "min_lat": 1.7575,
    "max_lat": 17.9578,
    "min_lng": 157.4121,
    "max_lng": 175.5395
  },
  "MP":
  {
    "name": "Northern Mariana Islands",
    "min_lat": 14.834442,
    "max_lat": 15.300557,
    "min_lng": 145.530052,
    "max_lng": 145.836296
  },
  "PW":
  {
    "name": "Palau",
    "min_lat": 1.7355,
    "max_lat": 11.4584,
    "min_lng": 129.6166,
    "max_lng": 136.9116
  },
  "PR":
  {
    "name": "Puerto Rico",
    "min_lat": 17.904834,
    "max_lat": 18.520551,
    "min_lng": -67.289886,
    "max_lng": -65.177765
  },
  "VI":
  {
    "name": "Virgin Islands",
    "min_lat": 18.302014,
    "max_lat": 18.751244,
    "min_lng": -64.861221,
    "max_lng": -64.26384
  }
}


def randomly_generated_cost_paid(year, state):
    row = data[(data['year'] == year) & (data['state'] == state)]
    avearge_mwg_per_customer = np.round(row['megawatthours'].values[0]/row['customers'].values[0],4)
    price = row['price'].values[0]
    randomly_generated_cost_paid = np.random.normal(avearge_mwg_per_customer*price, STATE_STDs[state])
    return randomly_generated_cost_paid

def randomly_nudge_location(state):
    bounds = STATE_BOUNDS[state]
    lat = np.random.uniform(bounds["min_lat"], bounds["max_lat"])
    lng = np.random.uniform(bounds["min_lng"], bounds["max_lng"])
    return lat, lng

def get_avg_temp_from_year(year, state):
    row = data[(data['year'] == year) & (data['state'] == state)]
    return row['average_temp'].values[0]

# Function to generate synthetic profiles
def generate_synthetic_profiles(data, num_profiles=1000):
    """
    Generate synthetic consumer profiles based on the given dataset.

    Args:
        data (DataFrame): Dataset to use as a basis for generating profiles.
        num_profiles (int): Number of profiles to generate.

    Returns:
        list: List of dictionaries representing synthetic profiles.
    """
    profiles = []
    for i in tqdm(range(num_profiles), desc="Generating profiles"):
        # Generate a synthetic name
        name = f"User_{random.randint(1000, 9999)}"
        
        # Generate a unique ID
        id_number = f"{i+1:05d}"
        
        # Randomly select a state from the dataset
        state = random.choice(data['state'].unique())
        
        # Generate random energy expenditure data from 2010 to 2022
        years = range(2010, 2023)
        money_spent = {
            str(year): randomly_generated_cost_paid(year, state) for year in years
        }


        
        lat, lng = randomly_nudge_location(state)
        # Create the profile dictionary
        profile = {
            "name": name,
            "id": id_number,
            "state": state,
            "money_spent": money_spent,
            "lat": lat,
            "lng": lng
        }

        for year in years:
            profile[f"money_spent_{str(year)}"] = money_spent[str(year)]
            profile[f"average_temperature_{str(year)}"] = get_avg_temp_from_year(year, state)

        profiles.append(profile)
    
    return profiles

if __name__ == "__main__":
  # Generate profiles
  synthetic_profiles = generate_synthetic_profiles(data, num_profiles=1000)

  # Save the profiles to a JSON file
  output_path = "synthetic_profiles.json"
  with open(output_path, "w") as f:
      json.dump(synthetic_profiles, f, indent=4)

  print(f"Synthetic profiles saved to {output_path}")
