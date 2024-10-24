import json
import os

def check_multiple_test_pairs(directory='../dataset/training'):
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as f:
                task_data = json.load(f)
                
                # Check if there are multiple test pairs
                num_test_pairs = len(task_data.get('test', []))
                if num_test_pairs > 1:
                    print(f"File: {filename} has {num_test_pairs} test pairs.")

# Call the function
check_multiple_test_pairs()
