def count_prediction_differences(file1, file2, show_diffs=False):
    def load_predictions(path):
        data = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.lower().startswith("document id"):
                    continue
                parts = [x.strip() for x in line.split(',')]
                if len(parts) != 2:
                    continue
                sid, pred = parts
                data[sid] = pred
        return data

    preds1 = load_predictions(file1)
    preds2 = load_predictions(file2)

    if preds1.keys() != preds2.keys():
        raise ValueError("Mismatch in sentence IDs between files.")

    # Separate counters
    exact_match = 0
    diff_plus_minus_1 = 0  # Differences of exactly ±1
    diff_larger_than_1 = 0  # Differences > 1
    
    for sid in preds1:
        try:
            # Try to convert to numbers
            num1 = float(preds1[sid])
            num2 = float(preds2[sid])
            diff = abs(num1 - num2)
            
            if diff == 0:
                exact_match += 1
            elif diff == 1:
                diff_plus_minus_1 += 1
                if show_diffs:
                    print(f"ID {sid}: {preds1[sid]} (file1) vs {preds2[sid]} (file2) [DIFF: ±1]")
            elif diff > 1:
                diff_larger_than_1 += 1
                if show_diffs:
                    print(f"ID {sid}: {preds1[sid]} (file1) vs {preds2[sid]} (file2) [DIFF: {diff:.1f}]")
                    
        except ValueError:
            # If can't convert to numbers, do string comparison
            if preds1[sid] == preds2[sid]:
                exact_match += 1
            else:
                diff_larger_than_1 += 1  # Treat string differences as significant
                if show_diffs:
                    print(f"ID {sid}: {preds1[sid]} (file1) vs {preds2[sid]} (file2) [STRING DIFF]")

    # Print summary
    total_predictions = len(preds1)
    print(f"\n{'='*50}")
    print(f"PREDICTION COMPARISON SUMMARY")
    print(f"{'='*50}")
    print(f"Total predictions: {total_predictions}")
    print(f"Exact matches (diff = 0): {exact_match} ({exact_match/total_predictions*100:.1f}%)")
    print(f"Small differences (diff = ±1): {diff_plus_minus_1} ({diff_plus_minus_1/total_predictions*100:.1f}%)")
    print(f"Large differences (diff > 1): {diff_larger_than_1} ({diff_larger_than_1/total_predictions*100:.1f}%)")
    print(f"{'='*50}")
    
    return {
        'exact_match': exact_match,
        'diff_plus_minus_1': diff_plus_minus_1,
        'diff_larger_than_1': diff_larger_than_1,
        'total': total_predictions
    }

# Example usage
results = count_prediction_differences("prediction1.csv", "prediction2.csv", show_diffs=True)

# Additional analysis
print(f"\nADDITIONAL ANALYSIS:")
print(f"Models agree exactly or within ±1: {results['exact_match'] + results['diff_plus_minus_1']} cases ({(results['exact_match'] + results['diff_plus_minus_1'])/results['total']*100:.1f}%)")
print(f"Models disagree significantly: {results['diff_larger_than_1']} cases ({results['diff_larger_than_1']/results['total']*100:.1f}%)")
