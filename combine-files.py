import json
import os

def combine_files_to_json(input_dir, output_file):
    combined_data = {}

    # Read all JSON files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(input_dir, filename)
            task_id = filename.split('.')[0]
            with open(file_path, 'r') as f:
                task_data = json.load(f)
            combined_data[task_id] = task_data

    # Write the combined data to the output file
    with open(output_file, 'w') as f:
        json.dump(combined_data, f, indent=2)

    print(f"Combined {len(combined_data)} tasks into {output_file}")

# Usage
input_dir = './testy'
output_file = 'arc-agi_test_challenges.json'
combine_files_to_json(input_dir, output_file)
