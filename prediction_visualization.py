import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_readability_distribution(csv_file_path):
    """
    Read CSV file and analyze the distribution of Readability_Level_19 column
    """
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Display basic information about the dataset
    print("Dataset Info:")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print("\nColumn names:")
    print(df.columns.tolist())
    
    # Check for missing values in Readability_Level_19
    print(f"\nMissing values in Readability_Level_19: {df['Readability_Level_19'].isnull().sum()}")
    
    # Get the distribution of Readability_Level_19
    readability_distribution = df['Readability_Level_19'].value_counts().sort_index()
    readability_percentage = df['Readability_Level_19'].value_counts(normalize=True).sort_index() * 100
    
    # Create a summary DataFrame
    distribution_summary = pd.DataFrame({
        'Readability_Level': readability_distribution.index,
        'Count': readability_distribution.values,
        'Percentage': readability_percentage.values
    })
    
    print("\n" + "="*50)
    print("READABILITY LEVEL 19 DISTRIBUTION")
    print("="*50)
    print(distribution_summary.to_string(index=False, float_format='%.2f'))
    
    # Create visualizations
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar plot
    sns.countplot(data=df, x='Readability_Level_19', ax=axes[0], order=sorted(df['Readability_Level_19'].unique()))
    axes[0].set_title('Distribution of Readability Level 19 (Count)')
    axes[0].set_xlabel('Readability Level 19')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Pie chart
    axes[1].pie(readability_distribution.values, labels=readability_distribution.index, autopct='%1.1f%%')
    axes[1].set_title('Distribution of Readability Level 19 (Percentage)')
    
    plt.tight_layout()
    plt.show()
    
    return df, distribution_summary

# Usage example
if __name__ == "__main__":
    csv_file_path = 'usedData\D3TOK_Preprocessed_BAREC_Dataset2.csv'
    
    try:
        df, summary = analyze_readability_distribution(csv_file_path)
        
        # Additional analysis
        print("\n" + "="*50)
        print("ADDITIONAL STATISTICS")
        print("="*50)
        print(f"Most common readability level: {summary.iloc[0]['Readability_Level']} ({summary.iloc[0]['Count']} samples)")
        print(f"Least common readability level: {summary.iloc[-1]['Readability_Level']} ({summary.iloc[-1]['Count']} samples)")
        print(f"Level imbalance ratio: {summary.iloc[0]['Count'] / summary.iloc[-1]['Count']:.2f}:1")
        
        # Show basic statistics
        print(f"\nReadability Level 19 Statistics:")
        print(f"Mean: {df['Readability_Level_19'].mean():.2f}")
        print(f"Median: {df['Readability_Level_19'].median():.2f}")
        print(f"Min: {df['Readability_Level_19'].min()}")
        print(f"Max: {df['Readability_Level_19'].max()}")
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        print("Please make sure the file path is correct.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
