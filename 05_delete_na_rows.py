#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd

def process_csv_file(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Check for NaN values in the specified columns
    rows_with_nan = df.isna().any(axis=1)

    # Remove rows with NaN values
    df = df[~rows_with_nan]

    # Save the modified DataFrame to a new CSV file
    base_filename, extension = os.path.splitext(file_path)
    output_file_path = f"{base_filename}.csv"
    df.to_csv(output_file_path, index=False)

def process_csv_files(directory_path):
    # List all files in the directory
    file_list = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

    # Process each CSV file
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        process_csv_file(file_path)

# Specify the directory containing CSV files
directory_path = '/Users/nicolaslewagon/spinjoy/csv_files'

# Process all CSV files in the directory
process_csv_files(directory_path)

