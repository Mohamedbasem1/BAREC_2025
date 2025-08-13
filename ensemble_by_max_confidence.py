import pandas as pd
import numpy as np

def ensemble_by_max_confidence_simple(file1_path, file2_path, output_path):
    """
    Ensemble two CSV files by selecting the result with higher confidence for each ID
    Output only contains ID and Predicted_Level
    
    Parameters:
    file1_path (str): Path to first CSV file
    file2_path (str): Path to second CSV file
    output_path (str): Path to save ensemble results
    """
    
    try:
        # Read the CSV files
        print("Reading CSV files...")
        df1 = pd.read_csv(file1_path, encoding='utf-8')
        df2 = pd.read_csv(file2_path, encoding='utf-8')
        
        print(f"File 1: {len(df1)} records")
        print(f"File 2: {len(df2)} records")
        
        # Merge dataframes on ID to compare
        merged_df = pd.merge(df1, df2, on='ID', suffixes=('_model1', '_model2'))
        print(f"Common IDs: {len(merged_df)}")
        
        # Initialize result list
        ensemble_results = []
        
        # For each row, select the one with higher confidence
        for _, row in merged_df.iterrows():
            conf1 = row['Confidence_model1']
            conf2 = row['Confidence_model2']
            
            if conf1 >= conf2:
                # Select prediction from model 1
                selected_prediction = row['Predicted_Level_model1']
                selected_from = 'Model1'
            else:
                # Select prediction from model 2
                selected_prediction = row['Predicted_Level_model2']
                selected_from = 'Model2'
            
            # Create simple result row with only ID and Prediction
            selected_row = {
                'ID': row['ID'],
                'Prediction': selected_prediction
            }
            
            ensemble_results.append(selected_row)
        
        # Create result dataframe
        result_df = pd.DataFrame(ensemble_results)
        
        # Sort by ID to maintain order
        result_df = result_df.sort_values('ID').reset_index(drop=True)
        
        # Save to CSV
        result_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"\nEnsemble completed successfully!")
        print(f"Results saved to: {output_path}")
        print(f"Total records in ensemble: {len(result_df)}")
        
        # Print statistics (using merged_df for analysis)
        print_ensemble_statistics_simple(merged_df)
        
        return result_df
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def print_ensemble_statistics_simple(merged_df):
    """
    Print statistics about the ensemble results
    """
    print("\n" + "="*50)
    print("ENSEMBLE STATISTICS")
    print("="*50)
    
    # Count how many times each model would be selected
    model1_selected = (merged_df['Confidence_model1'] >= merged_df['Confidence_model2']).sum()
    model2_selected = len(merged_df) - model1_selected
    
    print(f"Selected from Model 1: {model1_selected} ({model1_selected/len(merged_df)*100:.1f}%)")
    print(f"Selected from Model 2: {model2_selected} ({model2_selected/len(merged_df)*100:.1f}%)")
    
    # Calculate ensemble average confidence
    ensemble_confidence = np.where(
        merged_df['Confidence_model1'] >= merged_df['Confidence_model2'],
        merged_df['Confidence_model1'],
        merged_df['Confidence_model2']
    )
    avg_ensemble_confidence = ensemble_confidence.mean()
    
    # Compare with individual model averages
    avg_conf1 = merged_df['Confidence_model1'].mean()
    avg_conf2 = merged_df['Confidence_model2'].mean()
    
    print(f"Average confidence in ensemble: {avg_ensemble_confidence:.4f}")
    print(f"Model 1 average confidence: {avg_conf1:.4f}")
    print(f"Model 2 average confidence: {avg_conf2:.4f}")
    
    # Confidence improvement
    max_individual_avg = max(avg_conf1, avg_conf2)
    improvement = ((avg_ensemble_confidence - max_individual_avg) / max_individual_avg) * 100
    print(f"Confidence improvement: {improvement:.2f}%")
    
    # Get ensemble predictions
    ensemble_predictions = np.where(
        merged_df['Confidence_model1'] >= merged_df['Confidence_model2'],
        merged_df['Predicted_Level_model1'],
        merged_df['Predicted_Level_model2']
    )
    
    # Level distribution in ensemble
    print(f"\nPredicted Level Distribution in Ensemble:")
    unique_levels, counts = np.unique(ensemble_predictions, return_counts=True)
    for level, count in zip(unique_levels, counts):
        print(f"Level {level}: {count} ({count/len(ensemble_predictions)*100:.1f}%)")
    
    # Agreement between models
    agreement = (merged_df['Predicted_Level_model1'] == merged_df['Predicted_Level_model2']).sum()
    print(f"\nModel Agreement: {agreement}/{len(merged_df)} ({agreement/len(merged_df)*100:.1f}%)")

def quick_ensemble_id_prediction_only(file1_path, file2_path, output_path):
    """
    Ultra-simple version - just ID and Prediction columns
    """
    try:
        # Read files
        df1 = pd.read_csv(file1_path, encoding='utf-8')
        df2 = pd.read_csv(file2_path, encoding='utf-8')
        
        # Merge on ID
        merged = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))
        
        # Select based on confidence
        mask = merged['Confidence_1'] >= merged['Confidence_2']
        selected_predictions = np.where(mask, 
                                      merged['Predicted_Level_1'], 
                                      merged['Predicted_Level_2'])
        
        # Create simple result
        result = pd.DataFrame({
            'ID': merged['ID'],
            'Prediction': selected_predictions
        })
        
        # Sort by ID
        result = result.sort_values('ID').reset_index(drop=True)
        
        # Save to CSV
        result.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"Simple ensemble saved to: {output_path}")
        print(f"Total records: {len(result)}")
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # File paths - update these with your actual file paths
    file1_path = "arabertv2_ordinal_detailed_predictions.csv"
    file2_path = "arabertv2_oll15_detailed_predictions.csv"
    output_path = "ensemble_id_prediction.csv"
    
    print("Starting ensemble process...")
    print("Method: Select result with highest confidence for each ID")
    print("Output: ID and Prediction columns only")
    print("-" * 60)
    
    # Simple ensemble with only ID and Prediction
    result_df = ensemble_by_max_confidence_simple(file1_path, file2_path, output_path)
    
    if result_df is not None:
        print("\n" + "="*60)
        print("SAMPLE RESULTS")
        print("="*60)
        print(result_df.head(10))
        
        print(f"\nOutput file structure:")
        print(f"Columns: {list(result_df.columns)}")
        print(f"Shape: {result_df.shape}")
        
    # Alternative ultra-quick version
    print(f"\n" + "-"*40)
    print("Creating ultra-quick version...")
    quick_output = "quick_ensemble_id_prediction.csv"
    quick_result = quick_ensemble_id_prediction_only(file1_path, file2_path, quick_output)
    
    if quick_result is not None:
        print("Quick version sample:")
        print(quick_result.head(5))
