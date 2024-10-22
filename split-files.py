import json
import os

def split_json_to_files(input_file, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Split into individual files
    for task_id, task_data in data.items():
        output_file = os.path.join(output_dir, f"{task_id}.json")
        with open(output_file, 'w') as f:
            json.dump(task_data, f, indent=2)

    print(f"Split {len(data)} tasks into individual files in {output_dir}")

# Usage
input_file = '../arc4/data/arc-prize-2024/arc-agi_test_challenges.json'
output_dir = 'dataset/test'
split_json_to_files(input_file, output_dir)
