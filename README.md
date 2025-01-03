# Hotel Allocation Project

## Overview
The Hotel Allocation Project is designed to allocate guests to hotels using four different strategies. The project aims to find the best allocation strategy that maximizes guest satisfaction and hotel revenue. This project includes data analysis, multiple allocation methods, and visualization of the results to determine the most efficient strategy.

## Project Structure
The project is organized into several modules, each responsible for a different part of the process:

- **main.py**: The main script that coordinates the execution of different modules, including data loading, allocation strategies, and visualization.
- **modules/data_loading.py**: Functions for loading and preparing data from Excel files.
- **modules/allocation_strategies.py**: Contains four different strategies for allocating guests to hotels:
  - Random Allocation
  - Preference Allocation
  - Price Allocation
  - Availability Allocation
- **modules/visualization.py**: Functions for visualizing the results of each allocation strategy.
- **data/**: Contains input data files (`hotels.xlsx`, `guests.xlsx`, `preferences.xlsx`).
- **results/**: Stores the results of each allocation strategy and the generated visualizations.
- **requirements.txt**: Lists all dependencies needed to run the project.

## Allocation Strategies
The project uses four different strategies to allocate guests to hotels:

1. **Random Allocation**: Assigns guests to available hotels randomly.
2. **Preference Allocation**: Allocates guests based on their preferences for specific hotels.
3. **Price Allocation**: Assigns guests to the cheapest available hotel that meets their requirements.
4. **Availability Allocation**: Allocates guests based on room availability, starting with hotels that have the most rooms available.

## How to Run the Project
To run the project, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone <https://github.com/Laura-shul/HotelProjectLaura.git>
   ```
2. **Navigate to the project directory**:
   ```sh
   cd HotelAllocationProject
   ```
3. **Create and activate a virtual environment**:
   - For Windows:
     ```sh
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - For macOS/Linux:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```
4. **Install the required dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
5. **Run the main script**:
   ```sh
   python main.py
   ```

## Results and Visualization
The results of each allocation strategy are saved as CSV files in the `data/` folder. Additionally, an enhanced visualization comparing the revenue and effectiveness of each strategy is saved in the `results/` folder as `enhanced_revenue_comparison.png`.

## Analysis and Presentation
The project includes a Jupyter Notebook (`Hotel_Allocation_Analysis.ipynb`) that can be used for further analysis of the results and to create additional visualizations. This is particularly useful for understanding the effectiveness of each strategy and preparing for a presentation.
