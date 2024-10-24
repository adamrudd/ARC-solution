import os
import csv

# Define the paths
training_path = "../dataset/training"
model_outputs_path = "../model_outputs"

# Get the filenames from both directories
training_files = set(f.rsplit('.', 1)[0] for f in os.listdir(training_path) if f.endswith('.json'))
model_output_files = set(f.rsplit('.', 1)[0] for f in os.listdir(model_outputs_path) if f.endswith('.json'))

# Combine all unique filenames
all_files = training_files.union(model_output_files)

# Create a list to hold all the data
data = []

# Prepare the data
for filename in all_files:
    in_training = filename in training_files
    in_model_outputs = filename in model_output_files
    in_both = in_training and in_model_outputs
    data.append([filename, in_training, in_model_outputs, in_both])

# Sort the data based on the 'In Both' column (True first, then False)
data.sort(key=lambda x: (not x[3], x[0]))

# Create the CSV file
with open('file_comparison.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header
    writer.writerow(['Filename', 'In Training', 'In Model Outputs', 'In Both'])
    
    # Write the sorted data
    writer.writerows(data)

print("CSV file 'file_comparison.csv' has been created.")
