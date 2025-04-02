import pandas as pd
import os
import glob
import datetime

"""Merge CSVs with different column orders into one, adding a column to track the source file."""

# Path to the folder containing the CSV files
folder_path = "C:/Users/lmd8/OneDrive - Rice University/Desktop/DSpace/collection_exports"

ROOT_FILE_NAME = "csv_merge"
TIMESTAMP = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')

# Get a list of all CSV files in the directory
file_list = glob.glob(os.path.join(folder_path, "*.csv"))
print(file_list)

# Create an empty DataFrame to hold all the merged data
master_df = pd.DataFrame()

# Loop through each file in the file list
for file in file_list:
    # Read the current CSV file, treating all columns as strings
    df = pd.read_csv(file, dtype=str, low_memory=False)

    # Add a column to the DataFrame with the source file name
    file_name = os.path.basename(file)  # Extract just the file name (no path)
    df['source_file'] = file_name  # Add the file name as a new column

    # Append the data to the master DataFrame
    master_df = pd.concat([master_df, df], ignore_index=True, sort=False)

# Check if the parent directory exists, or create one if missing
parent_folder = os.path.dirname(folder_path)

if not os.path.exists(parent_folder):
    os.makedirs(parent_folder)

# Save the merged data to a new CSV file in the parent folder
output_file = os.path.join(parent_folder, f"{ROOT_FILE_NAME}{TIMESTAMP}.csv")
master_df.to_csv(output_file, index=False)