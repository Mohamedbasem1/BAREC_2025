import pandas as pd
import numpy as np

def combine_csv_highest_confidence(file1_path: str,
                                   file2_path: str,
                                   output_path: str = "combined_highest_confidence.csv") -> pd.DataFrame:
    """
    Merge two CSVs that each contain the columns:
      Sentence_ID, Prediction, Highest_Conf_Value
    For every Sentence_ID:
    1. Keep only rows with the highest Highest_Conf_Value
    2. If multiple rows have the same highest confidence, average their Predictions
    """
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    # Concatenate the dataframes
    combined = pd.concat([df1, df2], ignore_index=True)
    
    print(f"📊 Total rows after combining: {len(combined):,}")
    
    # Group by Sentence_ID and process each group
    result_rows = []
    averaging_cases = 0
    
    for sentence_id, group in combined.groupby('Sentence_ID'):
        # Find the maximum confidence value for this sentence
        max_conf = group['Highest_Conf_Value'].max()
        
        # Get rows with the maximum confidence
        max_conf_rows = group[group['Highest_Conf_Value'] == max_conf]
        
        if len(max_conf_rows) == 1:
            # Only one row with max confidence - keep it as is
            result_rows.append(max_conf_rows.iloc[0])
        else:
            # Multiple rows with same max confidence - average the predictions
            averaging_cases += 1
            avg_prediction = max_conf_rows['Prediction'].mean()
            
            # Create a new row with averaged prediction
            new_row = max_conf_rows.iloc[0].copy()  # Take first row as template
            new_row['Prediction'] = round(avg_prediction)  # Round to nearest integer
            
            result_rows.append(new_row)
            
            print(f"🔀 Sentence_ID {sentence_id}: Averaged {len(max_conf_rows)} predictions "
                  f"{list(max_conf_rows['Prediction'])} → {round(avg_prediction)} (conf={max_conf:.4f})")
    
    # Convert back to DataFrame
    best_rows = pd.DataFrame(result_rows)
    best_rows = best_rows.sort_values('Sentence_ID').reset_index(drop=True)
    
    # **FIX: Convert integer columns to proper int type to remove .0**
    best_rows['Sentence_ID'] = best_rows['Sentence_ID'].astype('int64')
    best_rows['Prediction'] = best_rows['Prediction'].astype('int64')
    
    # Save results with proper integer formatting
    best_rows.to_csv(output_path, index=False, float_format='%.4f')
    
    print(f"✅ Saved {len(best_rows):,} unique sentences to {output_path}")
    print(f"📈 Averaging applied to {averaging_cases} sentences with tied confidence values")
    
    return best_rows

# Run it on your two files
result = combine_csv_highest_confidence(
            "Average_Weighted_Predictions_2Models.csv",
            "Average Weighted Predictions_4models.csv",
            "combined.csv"
         )

# Show statistics
print(f"\n📊 FINAL RESULTS:")
print(f"Total unique sentences: {len(result):,}")
print(f"\nPrediction distribution:")
pred_dist = result['Prediction'].value_counts().sort_index()

print(f"\nConfidence statistics:")
print(f"Average confidence: {result['Highest_Conf_Value'].mean():.4f}")
print(f"Min confidence: {result['Highest_Conf_Value'].min():.4f}")
print(f"Max confidence: {result['Highest_Conf_Value'].max():.4f}")

# Show a sample with proper integer formatting
print(f"\n📋 Sample results:")
sample_df = result.head(10).copy()
# Format for display without .0
sample_df['Sentence_ID'] = sample_df['Sentence_ID'].astype('int64')
sample_df['Prediction'] = sample_df['Prediction'].astype('int64')
print(sample_df.to_string(index=False))
