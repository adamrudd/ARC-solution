import os
import json
import re

# Function to parse the grid from a string
def parse_grid(line):
    parts = line.strip().split('|')
    # Convert each part (except the last one) into a list of integers
    grid = [list(map(int, part.strip())) for part in parts[:-1] if part.strip()]  # Exclude empty parts
    # Get the score from the last part
    score = float(parts[-1].strip())
    return grid, score

# Function to process each CSV file and extract the required information
def process_csv_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    task_info = []
    task_id_output_number = lines[0].strip()  # First line contains taskID_outputNumber
    task_id, output_number = task_id_output_number.split('_')

    # Convert output_number to an integer and start from 1
    output_number = int(output_number) + 1  # Start from 1 instead of 0

    # Iterate through each attempt line
    for attempt_number, line in enumerate(lines[1:], start=1):
        if line.strip():  # Ensure the line is not empty
            grid, score = parse_grid(line)  # Parse grid and score
            
            # Create the label
            model_number = re.search(r'answer_\d+_(\d+)', file_path).group(1)
            label = f"Output {output_number} Model {model_number} Attempt {attempt_number}"
            
            # Append to task info
            task_info.append({
                "grid": grid,
                "score": score,
                "label": label
            })
    
    return task_id, task_info

# Main function to convert all CSV files in a directory to JSON format
def convert_directory_to_json(input_dir, output_dir):
    task_data = {}

    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            task_id, attempts = process_csv_file(file_path)
            
            if task_id not in task_data:
                task_data[task_id] = []
            
            task_data[task_id].extend(attempts)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write the output to JSON files
    for task_id, data in task_data.items():
        output_file_path = os.path.join(output_dir, f"{task_id}.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

# Specify the input and output directories
input_dir = '../output'
output_dir = '../model_outputs'
convert_directory_to_json(input_dir, output_dir)
