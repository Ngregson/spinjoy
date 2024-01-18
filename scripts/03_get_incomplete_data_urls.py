#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
from datetime import datetime

# Define paths and file name pattern
spinjoy_path = '/Users/nicolaslewagon/spinjoy/'
incomplete_path = f'{spinjoy_path}/csv_files/incomplete/'
file_pattern = '*_incomplete.csv'

# Use glob to get a list of file paths matching the pattern
file_paths = glob.glob(incomplete_path + file_pattern)

# Initialize an empty list to store individual "incomplete data" DataFrames
dfs_incomplete = []

# Initialize an empty list to store individual "complete data" DataFrames
dfs_full = []

# Iterate over the files
for file_path in file_paths:
    
    # Retrieve seller name
    part = file_path.split('_')
    sellers = '_'.join(part[3:-5])
    
    # Load each CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Define the columns where to check the na values
    columns_to_check = [
        'nb_for_sale',
        'current_lowest_price',
        'have',
        'want',
        'avg_rating',
        'ratings',
        'last_sold_date',
        'low_price',
        'median_price',
        'high_price']
    
    # Define the columns to keep for the df of incomplete datas
    columns_to_keep = [
        'seller', 
        'release_url',
        'media_condition',
        'sleeve_condition',
        'price',
        'img_url',
        'format_detail',
        'nb_for_sale',
        'current_lowest_price']

    # Define df_incomplete_datas
    rows_with_nan = df[columns_to_check].isna().any(axis=1)
    filtered_df = df[rows_with_nan]
    df_incomplete_datas = filtered_df.loc[:, columns_to_keep]

    # Add each df_incomplete_datas in dfs_incomplete
    dfs_incomplete.append(df_incomplete_datas)

    # Define df_complete_datas 
    df_complete_datas = df[~rows_with_nan]

    # Add each df_complete_datas in dfs_full
    dfs_full.append(df_complete_datas)

#Concatenate the dfs of the list dfs_incomplete
df_incomplete_data_urls = pd.concat(dfs_incomplete, ignore_index=True)

#Concatenate the dfs of the list dfs_incomplete
df_data_full = pd.concat(dfs_full, ignore_index=True)

# Get the current date
current_date = datetime.now().date()

# Get the current time
current_time = datetime.now().time().strftime("%Hh%M")

#Export df_incomplete_data_urls in the releases_urls folder
df_incomplete_data_urls.to_csv(f'{spinjoy_path}releases_urls/releases_urls_incomplete_{current_date}_{current_time}.csv', index=False)

#Export df_complete_data_urls in the csv_files folder
df_data_full.to_csv(f'{spinjoy_path}csv_files/datas_discogs_part_incomplete_{current_date}_{current_time}_full.csv', index=False)

