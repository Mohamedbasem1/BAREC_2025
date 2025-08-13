def ensemble_by_averaging(file1, file2, output_file, rounding="round"):
    def load_predictions(path):
        preds = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if not line or line.lower().startswith("sentence id"):
                    continue
                parts = [x.strip() for x in line.split(",")]
                if len(parts) != 2:
                    continue
                sid, pred = parts
                preds[sid] = int(pred)
        return preds

    preds1 = load_predictions(file1)
    preds2 = load_predictions(file2)

    if preds1.keys() != preds2.keys():
        raise ValueError("Sentence IDs don't match between files.")

    used_first_file = 0
    used_higher_value = 0  # New counter for when we pick higher value
    used_average = 0

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("Sentence ID,Prediction\n")
        for sid in preds1:
            diff = abs(preds1[sid] - preds2[sid])
            
            if diff == 0:
                # Exact match - use either value (they're the same)
                final_pred = preds1[sid]
                used_first_file += 1
            elif diff == 1:
                # Difference of exactly 1 - use the higher value
                final_pred =max( preds1[sid], preds2[sid])
                used_higher_value += 1
            else:
                # Calculate average when difference > 1
                avg = (preds1[sid] + preds2[sid]) / 2
                if rounding == "floor":
                    final_pred = int(avg // 1)
                elif rounding == "ceil":
                    final_pred = int(-1 * (-avg // 1))
                else:  # default to round
                    final_pred = round(avg)
                used_average += 1
            
            out.write(f"{sid},{final_pred}\n")

    print(f"Averaged ensemble saved to: {output_file}")
    print(f"Used first file prediction (exact match): {used_first_file} cases")
    print(f"Used higher value (diff = 1): {used_higher_value} cases")
    print(f"Used averaged prediction (diff > 1): {used_average} cases")

# Example usage
ensemble_by_averaging("prediction.csv", "prediction2.csv", 
    "prediction_maxx.csv",
    rounding="round"  # options: "round", "floor", "ceil"
)
