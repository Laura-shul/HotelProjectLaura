# data_loading.py: Functions for loading and processing data

import os
import logging
import pandas as pd

def load_and_prepare_data(base_dir, file_name, index_col=None, drop_cols=None):
    file_path = os.path.join(base_dir, file_name)
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            logging.error('Loaded DataFrame from %s is empty.', file_name)
            print(f"Warning: Loaded DataFrame from {file_name} is empty.")
        else:
            logging.info('DataFrame from %s loaded successfully with %d records.', file_name, len(df))
        if drop_cols:
            cols_to_drop = [col for col in drop_cols if col in df.columns]
            if cols_to_drop:
                df = df.drop(columns=cols_to_drop)  # Drop unnecessary columns
                logging.info('Dropped columns %s from %s', cols_to_drop, file_name)
        if index_col and index_col in df.columns:
            df.set_index(index_col, inplace=True)  # Set specified column as index
            logging.info('Set column %s as index for %s', index_col, file_name)
        return df
    except FileNotFoundError as err:
        logging.error('File not found: %s - %s', file_name, err)
        print(f"Error: File not found - {file_name}")
        return pd.DataFrame()
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as err:
        logging.error('Error loading data from %s - %s', file_name, err)
        print(f"Error: Could not load data from {file_name}")
        return pd.DataFrame()
    except PermissionError as err:
        logging.error('Permission denied: %s - %s', file_name, err)
        print(f"Error: Permission denied for file - {file_name}")
        return pd.DataFrame()

def check_data(df, name):
    if df.empty:
        logging.error('%s DataFrame is empty.', name)
        print(f"Error: {name} DataFrame is empty.")
    else:
        logging.info('%s DataFrame loaded successfully with %d records.', name, len(df))
        print(f"{name} DataFrame loaded successfully with {len(df)} records.")
    missing_values = df.isnull().sum()
    if missing_values.any():
        missing_values_filtered = missing_values[missing_values > 0]
        logging.warning('Missing values found in %s: %s', name, missing_values_filtered)
        print(f"Missing Values in {name}:\n{missing_values_filtered}")

