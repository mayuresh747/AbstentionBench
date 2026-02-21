import os
import json
import csv
from pathlib import Path

logs_dir = "/Users/mayuri/Documents/Projects/Abstention Bench/None/logs"
output_csv = "/Users/mayuri/Documents/Projects/Abstention Bench/all_results.csv"

all_data = []

# Walk through all directories in logs_dir
for root, dirs, files in os.walk(logs_dir):
    for file in files:
        if file == "GroundTruthAbstentionEvaluator.json" or file == "LLMJudgeAbstentionDetector.json":
            file_path = os.path.join(root, file)
            # Try to infer dataset name from path
            parts = file_path.split(os.sep)
            dataset_name = "Unknown"
            for part in parts:
                if "Dataset_" in part or part in ["UMWP_GPT51Rationalist", "GSM8K_GPT51Rationalist", "MMLUHistory_GPT51Rationalist", "MMLUMath_GPT51Rationalist", "GPQA_GPT51Rationalist"]:
                    dataset_name = part.split("_")[0]
                    break
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                if "responses" in data:
                    for item in data["responses"]:
                        prompt = item.get("prompt", {})
                        
                        question = prompt.get("question", "")
                        reference_answers = prompt.get("reference_answers", None)
                        should_abstain = prompt.get("should_abstain", None)
                        
                        response = item.get("response", "")
                        is_abstention = item.get("is_abstention", None)
                        is_abstention_correct = item.get("is_abstention_correct", None)
                        judge_response = item.get("full_judge_response", "")
                        
                        all_data.append({
                            "Dataset": dataset_name,
                            "Question": question,
                            "Reference Answers": str(reference_answers) if reference_answers else "",
                            "Should Abstain": should_abstain,
                            "Model Response": response,
                            "Judge Categorized as Abstention": is_abstention,
                            "Judge Explanation": judge_response,
                            "Is Abstention Correct": is_abstention_correct
                        })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

if all_data:
    # Remove duplicates if any (due to finding evaluating jsons)
    unique_data = []
    seen = set()
    for row in all_data:
        identifier = f"{row['Dataset']}_{row['Question']}"
        if identifier not in seen:
            seen.add(identifier)
            unique_data.append(row)

    print(f"Found {len(unique_data)} unique results. Writing to {output_csv}...")
    keys = unique_data[0].keys()
    with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(unique_data)
    print("Done!")
else:
    print("No data found to aggregate.")
