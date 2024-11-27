import pandas as pd
import json

def load_energy_data(file_path, file_type):
    """
    Load energy usage data from a file.

    Args:
        file_path (str): Path to the data file.
        file_type (str): Type of file ('csv' or 'json').

    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'json':
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'json'.")

def clean_data(df):
    """
    Clean and preprocess energy data.

    Args:
        df (pd.DataFrame): Raw data.

    Returns:
        pd.DataFrame: Cleaned data.
    """
    # Handle missing values
    df.fillna(0, inplace=True)

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Convert date columns to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Convert numeric columns to appropriate types
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].str.isnumeric().any():
            df[col] = pd.to_numeric(df[col])

    return df


