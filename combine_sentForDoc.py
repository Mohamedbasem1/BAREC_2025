import pandas as pd
import csv

def combine_predictions_to_max(input_csv_path, output_csv_path):
    """
    Reads a CSV with Sentence ID and Prediction columns,
    groups by first 7 digits of Sentence ID,
    finds max prediction for each group,
    and saves to new CSV.
    """
    
    # Read the input CSV
    df = pd.read_csv(input_csv_path)
    
    # Extract first 7 digits from Sentence ID
    df['Group_ID'] = df['Sentence ID'].astype(str).str[:7]
    
    # Group by first 7 digits and find max prediction
    result = df.groupby('Group_ID')['Prediction'].max().reset_index()
    
    # Rename columns for output
    result.columns = ['Sentence ID', 'Prediction']
    
    # Save to new CSV
    result.to_csv(output_csv_path, index=False)
    
    print(f"Results saved to {output_csv_path}")
    print(f"Number of groups: {len(result)}")
    print("\nSample output:")
    print(result.head())

# Alternative implementation without pandas (using only built-in libraries)
def combine_predictions_to_max_builtin(input_csv_path, output_csv_path):
    """
    Same functionality using only built-in Python libraries
    """
    
    # Dictionary to store max prediction for each group
    group_max = {}
    
    # Read input CSV
    with open(input_csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            sentence_id = row['Sentence ID']
            prediction = int(row['Prediction'])
            
            # Extract first 7 digits
            group_id = sentence_id[:7]
            
            # Update max for this group
            if group_id not in group_max:
                group_max[group_id] = prediction
            else:
                group_max[group_id] = max(group_max[group_id], prediction)
    
    # Write output CSV
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Sentence ID', 'Prediction'])
        
        # Write grouped results
        for group_id, max_prediction in sorted(group_max.items()):
            writer.writerow([group_id, max_prediction])
    
    print(f"Results saved to {output_csv_path}")
    print(f"Number of groups: {len(group_max)}")

# Usage example
if __name__ == "__main__":
    # Input and output file paths
    input_file = "Average Weighted Predictions_4models.csv"
    output_file = "combined_results.csv"
    
    # Method 1: Using pandas (recommended)
    try:
        combine_predictions_to_max(input_file, output_file)
    except ImportError:
        print("Pandas not available, using built-in method...")
        combine_predictions_to_max_builtin(input_file, output_file)
    
    # Method 2: Using only built-in libraries
    # combine_predictions_to_max_builtin(input_file, output_file)
