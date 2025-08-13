import pandas as pd
import numpy as np
from collections import Counter

def voting_ensemble(file_paths, output_file='final_prediction.csv', method='majority'):
    """
    Create voting ensemble from multiple prediction files
    
    Parameters:
    file_paths: list of CSV file paths
    output_file: output CSV file name
    method: 'majority' for majority voting, 'average' for average voting
    """
    
    # Read all prediction files
    predictions = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        predictions.append(df)
    
    # Merge all predictions on Document ID
    merged_df = predictions[0].copy()
    merged_df.columns = ['Document ID', 'Prediction_1']
    
    for i, pred_df in enumerate(predictions[1:], 2):
        pred_df.columns = ['Document ID', f'Prediction_{i}']
        merged_df = merged_df.merge(pred_df, on='Document ID', how='outer')
    
    # Apply voting mechanism
    if method == 'majority':
        # Majority voting
        def majority_vote(row):
            votes = [row[f'Prediction_{i}'] for i in range(1, len(predictions) + 1) if pd.notna(row[f'Prediction_{i}'])]
            if votes:
                vote_counts = Counter(votes)
                return vote_counts.most_common(1)[0][0]
            return np.nan
        
        merged_df['Prediction'] = merged_df.apply(majority_vote, axis=1)
    
    elif method == 'average':
        # Average voting (rounded to nearest integer)
        prediction_cols = [f'Prediction_{i}' for i in range(1, len(predictions) + 1)]
        merged_df['Prediction'] = merged_df[prediction_cols].mean(axis=1).round().astype(int)
    
    # Create final output
    final_df = merged_df[['Document ID', 'Prediction']].copy()
    final_df = final_df.dropna()  # Remove rows with missing predictions
    final_df['Document ID'] = final_df['Document ID'].astype(int)
    final_df['Prediction'] = final_df['Prediction'].astype(int)
    
    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"Voting ensemble saved to {output_file}")
    
    return final_df

# File paths for your three prediction files
file_paths = [
    '78.70_DOC_prediction.csv',
    '79.3_DOC_prediction.csv', 
    '78.90_DOC_prediction.csv'
]

# Create voting ensemble with majority voting
final_predictions_majority = voting_ensemble(file_paths, 'final_prediction_majority.csv', method='majority')

# Create voting ensemble with average voting
final_predictions_average = voting_ensemble(file_paths, 'final_prediction_average.csv', method='average')

# Display first few rows
print("\nFirst 5 rows of majority voting results:")
print(final_predictions_majority.head())

print("\nFirst 5 rows of average voting results:")
print(final_predictions_average.head())
