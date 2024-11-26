import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules.data_loading import load_and_prepare_data
from modules.allocation_strategies import (
    random_allocation,
    preference_allocation,
    price_allocation,
    availability_allocation_optimized,
)

# Constants
BASE_DIR = "data"

# Helper Functions
@st.cache_data
def load_all_data():
    """Loads and caches all required datasets."""
    hotels = load_and_prepare_data(BASE_DIR, "hotels.xlsx", index_col="hotel")
    guests = load_and_prepare_data(BASE_DIR, "guests.xlsx", index_col="guest")
    preferences = load_and_prepare_data(BASE_DIR, "preferences.xlsx")
    return hotels, guests, preferences

def perform_allocation(method, hotels, guests, preferences):
    """Executes the selected allocation strategy."""
    if method == "Random Allocation":
        return random_allocation(hotels.copy(), guests.copy())
    elif method == "Preference Allocation":
        return preference_allocation(hotels.copy(), guests.copy(), preferences.copy())
    elif method == "Price Allocation":
        return price_allocation(hotels.copy(), guests.copy())
    elif method == "Availability Allocation Optimized":
        return availability_allocation_optimized(hotels.copy(), guests.copy())
    else:
        return None

# Load Data
st.title("Hotel Allocation System")
try:
    hotels, guests, preferences = load_all_data()
    st.success("Data loaded successfully.")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar: Available Guest IDs
st.sidebar.header("Available Guest IDs")
st.sidebar.write(guests.index.tolist()[:10])  # Show the first 10 IDs

# Main App Layout
st.header("Allocate Guests to Hotels")

# Input: Guest ID
guest_id = st.text_input("Enter Guest ID (e.g., guest_1)")
if guest_id:
    guest_id = guest_id.strip()  # Remove extra spaces

# Dropdown: Allocation Method
allocation_method = st.selectbox(
    "Select Allocation Method",
    ["Random Allocation", "Preference Allocation", "Price Allocation", "Availability Allocation Optimized"],
)

# Button: Show Guest Allocation
if st.button("Show Allocation for Guest"):
    if guest_id and allocation_method:
        st.info(f"Checking allocation for Guest ID: {guest_id} using {allocation_method}...")
        try:
            result = perform_allocation(allocation_method, hotels, guests, preferences)
            if result:
                result_df = pd.DataFrame(result)
                
                # Check if the guest exists in the result
                guest_allocation = result_df[result_df["guest_id"] == guest_id]
                if not guest_allocation.empty:
                    st.success(f"Guest {guest_id} is allocated as follows:")
                    st.table(guest_allocation)
                else:
                    st.warning(f"Guest {guest_id} was not allocated to any hotel.")
            else:
                st.warning(f"No allocation results for method: {allocation_method}.")
        except Exception as e:
            st.error(f"Error during allocation: {e}")
    else:
        st.error("Please enter a valid Guest ID and select an allocation method.")

# Enhanced Visualization: Compare All Strategies
st.header("Revenue Comparison Across Strategies")
all_results = {}

# Run all strategies and collect results
for method in ["Random Allocation", "Preference Allocation", "Price Allocation", "Availability Allocation Optimized"]:
    try:
        result = perform_allocation(method, hotels, guests, preferences)
        if result:
            result_df = pd.DataFrame(result)
            all_results[method] = result_df["final_price"].sum()  # Collect revenue
    except Exception as e:
        st.warning(f"Could not calculate results for {method}: {e}")

# Plotting the comparison
if all_results:
    st.subheader("Total Revenue by Strategy")
    revenue_df = pd.DataFrame.from_dict(all_results, orient="index", columns=["Revenue"])
    st.bar_chart(revenue_df)

    # Highlight the most profitable strategy
    best_strategy = revenue_df["Revenue"].idxmax()
    st.success(f"The most profitable strategy is **{best_strategy}** with a revenue of ${revenue_df['Revenue'].max():,.2f}.")
