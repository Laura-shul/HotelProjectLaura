import matplotlib.pyplot as plt
import seaborn as sns

def plot_enhanced_visualization(results):
    strategy_names = list(results.keys())
    revenue_values = [results[strategy]['revenue'] for strategy in strategy_names]
    guests_allocated_values = [results[strategy]['guests_allocated'] for strategy in strategy_names]
    unique_hotels_used_values = [results[strategy]['unique_hotels_used'] for strategy in strategy_names]
    
    try:
        # Plot 1: Comparison of Total Revenue for All Strategies
        sns.barplot(x=strategy_names, y=revenue_values, palette='viridis')
        plt.legend([], [], frameon=False)
        plt.title('Total Revenue Comparison for All Strategies')
        plt.ylabel('Total Revenue ($)')
        plt.xlabel('Allocation Strategy')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('results/total_revenue_comparison.png')
        print("Total revenue comparison plot saved as 'results/total_revenue_comparison.png'.")

        # Plot 2: Comparison of Total Guests Allocated for All Strategies
        sns.barplot(x=strategy_names, y=guests_allocated_values, palette='plasma')
        plt.legend([], [], frameon=False)
        plt.title('Total Guests Allocated Comparison for All Strategies')
        plt.ylabel('Number of Guests Allocated')
        plt.xlabel('Allocation Strategy')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('results/total_guests_allocated_comparison.png')
        print("Total guests allocated comparison plot saved as 'results/total_guests_allocated_comparison.png'.")

        # Plot 3: Comparison of Unique Hotels Used for All Strategies
        sns.barplot(x=strategy_names, y=unique_hotels_used_values, palette='magma')
        plt.legend([], [], frameon=False)
        plt.title('Unique Hotels Used Comparison for All Strategies')
        plt.ylabel('Number of Unique Hotels Used')
        plt.xlabel('Allocation Strategy')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('results/unique_hotels_used_comparison.png')
        print("Unique hotels used comparison plot saved as 'results/unique_hotels_used_comparison.png'.")
    
    except (IOError, ValueError) as e:
        print(f"Error: Could not generate or save the visualization. Error: {e}")    
plt.close()
