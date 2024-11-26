# main.py: Main script to coordinate the execution of different modules

import logging
import pandas as pd
import matplotlib
from tqdm import tqdm

# Import custom modules
from modules.data_loading import load_and_prepare_data, check_data
from modules.allocation_strategies import random_allocation, preference_allocation, price_allocation, availability_allocation_optimized
import modules.visualization as viz

matplotlib.use('Agg')

# Setup logging
logging.basicConfig(filename='hotel_allocation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Starting Hotel Allocation Project')

# Load data from Excel files
BASE_DIR = 'data'

hotels = load_and_prepare_data(BASE_DIR, 'hotels.xlsx', index_col='hotel')
guests = load_and_prepare_data(BASE_DIR, 'guests.xlsx', index_col='guest')
preferences = load_and_prepare_data(BASE_DIR, 'preferences.xlsx')

# Check the data for issues
check_data(hotels, "Hotels")
check_data(guests, "Guests")
check_data(preferences, "Preferences")

# Fill missing values with default values
hotels.fillna({'rooms': 0, 'price': 0}, inplace=True)
guests.fillna({'discount': 0.0}, inplace=True)

# Define all allocation strategies
strategies = {
    "Random Allocation": random_allocation,
    "Preference Allocation": preference_allocation,
    "Price Allocation": price_allocation,
    "Availability Allocation": availability_allocation_optimized
}

# Execute and save results for each strategy
analysis_results = {}

for strategy_name, strategy_function in tqdm(strategies.items(), desc="Running strategies"):
    logging.info('Running %s', strategy_name)
    print("\nRunning %s..." % strategy_name)
    
    if strategy_name in ["Preference Allocation", "Availability Allocation Optimized"]:
        result = strategy_function(hotels.copy(), guests.copy(), preferences.copy())
    else:
        result = strategy_function(hotels.copy(), guests.copy())
        
    if result is None or not result:
        logging.error('The result for %s strategy is empty or None.', strategy_name)
        print("Error: The result for %s strategy is empty or None." % strategy_name)
        continue
        
    result_df = pd.DataFrame(result)
    
    if result_df.empty:
        logging.error('The result DataFrame for %s strategy is empty.', strategy_name)
        print("Error: The result DataFrame for %s strategy is empty." % strategy_name)
        continue
        
    # Ensure required columns are present
    for col in ['final_price', 'hotel_id']:
        if col not in result_df.columns:
            result_df[col] = None
            logging.warning('Column %s was missing and has been added with default None values for %s strategy. This may indicate an issue with the allocation function.', col, strategy_name)
    
    # Save results to CSV file
    result_filename = f"data/{strategy_name.replace(' ', '_').lower()}_results.csv"
    try:
        result_df.to_csv(result_filename, index=False)
        print("%s results saved to '%s'." % (strategy_name, result_filename))
        logging.info('%s results saved to %s', strategy_name, result_filename)
    except IOError as err:
        logging.error('Error saving file %s: %s', result_filename, err)
        print("Error: Could not save %s results to '%s'. Error: %s" % (strategy_name, result_filename, err))
    
    # Analyze results
    if 'final_price' in result_df.columns:
        total_revenue = result_df['final_price'].sum()
    else:
        total_revenue = 0
    total_guests = len(result_df)
    unique_hotels = result_df['hotel_id'].nunique() if 'hotel_id' in result_df.columns else 0
    
    analysis_results[strategy_name] = {
        'revenue': total_revenue,
        'guests_allocated': total_guests,
        'unique_hotels_used': unique_hotels
    }

# Visualization of results
logging.info('Starting visualization of results')
try:
    viz.plot_enhanced_visualization(analysis_results)
    logging.info('Visualization saved successfully')
except (IOError, ValueError) as err:
    logging.error('Error during visualization: %s', err)
    print("Error: Could not generate visualization. Error: %s" % err)