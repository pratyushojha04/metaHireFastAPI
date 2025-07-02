import pandas as pd
import csv
import os

# List of CSV files to combine
csv_files = [
    'google_interview_questions_1_to_50.csv',
    'google_interview_questions_51_to_100.csv',
    'google_interview_questions_100_to_150.csv',
    'google_interview_questions_151_to_200.csv',
    'google_interview_questions_200_to_246.csv'
]

# Initialize an empty list to store DataFrames
dfs = []

# Read each CSV file and append to the list
for file in csv_files:
    if os.path.exists(file):
        try:
            # Read CSV with quoting to handle commas in fields
            df = pd.read_csv(file, quoting=csv.QUOTE_ALL)
            dfs.append(df)
            print(f"Successfully read {file} ({len(df)} rows)")
        except pd.errors.ParserError as e:
            print(f"Error reading {file}: {e}")
            # Read the file manually to inspect problematic lines
            with open(file, 'r') as f:
                lines = f.readlines()
                print(f"Content of problematic lines in {file}:")
                for i, line in enumerate(lines, 1):
                    fields = line.strip().split(',')
                    if len(fields) != 11 and 30 <= i <= 40:  # Focus around line 36
                        print(f"Line {i} (fields={len(fields)}): {line.strip()}")
            # Attempt to read with skipping bad lines as a fallback
            try:
                df = pd.read_csv(file, quoting=csv.QUOTE_ALL, on_bad_lines='warn')
                dfs.append(df)
                print(f"Partially read {file} with {len(df)} rows (skipped bad lines)")
            except Exception as e2:
                print(f"Failed to read {file} even with skipping: {e2}")
    else:
        print(f"Warning: {file} not found, skipping.")

# Combine all DataFrames into one
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by 'id' to ensure correct order
    combined_df = combined_df.sort_values(by='id')
    
    # Remove duplicates if any (optional, based on ID)
    combined_df = combined_df.drop_duplicates(subset=['id'], keep='first')
    
    # Save the combined DataFrame to a new CSV file with quoting
    output_file = 'google_interview_questions_combined.csv'
    combined_df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
    print(f"Combined CSV file '{output_file}' created successfully with {len(combined_df)} rows.")
else:
    print("Error: No CSV files were found to combine.")