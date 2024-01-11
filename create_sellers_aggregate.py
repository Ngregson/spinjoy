#!/usr/bin/env python
# coding: utf-8

# In[216]:


import pandas as pd
import re
import glob

try:
    # Define the file pattern to match
    file_pattern = 'csv_files/*_full.csv'
    
    # Create a list of all the matching files
    sellers_files = glob.glob(file_pattern)
    
    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Loop through the sellers_files list and read each CSV file into a DataFrame
    for seller_file in sellers_files:
        df = pd.read_csv(seller_file,dtype={'price': str})
        dfs.append(df)
    
    # Create df_sellers_aggregate
    df_sellers_aggregate = pd.concat(dfs, ignore_index=True)
    
    # Stock nb of duplicates
    number_of_duplicates = df_sellers_aggregate.duplicated()
    
    # Remove the duplicates
    df_sellers_aggregate.drop_duplicates(inplace=True)
    
    #Handle ',' in the price that does not allow conversion to float type
    df_sellers_aggregate['price'] = df_sellers_aggregate['price'].str.replace(',', '')
    
    #Transform "media_condition" and "sleeve_condition"
    df_sellers_aggregate["media_condition"] = df_sellers_aggregate["media_condition"].str.replace(r'\([^)]*\)', '', regex=True)
    df_sellers_aggregate["sleeve_condition"] = df_sellers_aggregate["sleeve_condition"].str.replace(r'\([^)]*\)', '', regex=True)
    
    #Transform "nb_for_sale"
    df_sellers_aggregate["nb_for_sale"] = df_sellers_aggregate["nb_for_sale"].str.extract(r'(\d+)')
    
    #Transform prices and handle "--" values
    price_columns = ["current_lowest_price","low_price", "median_price", "high_price"]
    
    for column in price_columns:
        df_sellers_aggregate[f"{column}"] = df_sellers_aggregate[f"{column}"].str[1:]
        df_sellers_aggregate[f"{column}"] = df_sellers_aggregate[f"{column}"].str.replace(',', '')
        df_sellers_aggregate[f"{column}"] = df_sellers_aggregate[f"{column}"].replace('-', float('nan'))
    
    #Transform "avg_rating" and handle "--" values
    df_sellers_aggregate['avg_rating'] = df_sellers_aggregate['avg_rating'].str.split(' / ').str.get(0)
    df_sellers_aggregate['avg_rating'] = df_sellers_aggregate['avg_rating'].str.replace(',', '')
    df_sellers_aggregate['avg_rating'] = df_sellers_aggregate['avg_rating'].replace('--', float('nan'))
    
    #Change type
    float_data = ["price", "current_lowest_price","low_price", "median_price", "high_price","avg_rating"]
    for column in float_data:
        df_sellers_aggregate[f"{column}"] = df_sellers_aggregate[f"{column}"].astype(float)
    
    int_data = ["have", "want", "ratings","nb_for_sale"]
    for column in int_data:
        df_sellers_aggregate[f"{column}"] = df_sellers_aggregate[f"{column}"].astype(int)
    
    #Handle several date formats
    df_sellers_aggregate['last_sold_date'] = df_sellers_aggregate['last_sold_date'].str.replace('Sept', 'Sep')
    
    df_sellers_aggregate['new_last_sold_date']= None
    df_sellers_aggregate['format'] = 1
    df_sellers_aggregate.loc[df_sellers_aggregate['last_sold_date'].str.contains(','), 'format'] = 2
    df_sellers_aggregate.loc[df_sellers_aggregate['last_sold_date'] == "Never", 'format'] = None
    
    df_sellers_aggregate.loc[df_sellers_aggregate.format == 1, 'new_last_sold_date'] = pd.to_datetime(df_sellers_aggregate.loc[df_sellers_aggregate.format == 1, 'last_sold_date'], format = '%d %b %Y').dt.strftime('%Y-%m-%d')
    df_sellers_aggregate.loc[df_sellers_aggregate.format == 2, 'new_last_sold_date'] = pd.to_datetime(df_sellers_aggregate.loc[df_sellers_aggregate.format == 2, 'last_sold_date'], format = '%b %d, %Y').dt.strftime('%Y-%m-%d')
    
    df_sellers_aggregate.drop(columns=['last_sold_date','format'], inplace=True)
    df_sellers_aggregate.rename(columns={'new_last_sold_date': 'last_sold_date'}, inplace=True)
    
    df_sellers_aggregate['last_sold_date'] = pd.to_datetime(df_sellers_aggregate['last_sold_date'], format='%Y-%m-%d', errors = 'coerce')
    
    # Function to extract the release ID  from the release_url
    def extract_number(release_url):
        match = re.search(r'/(\d+)-', release_url)
        if match:
            return match.group(1)
        else:
            return None
    
    # Apply the function to create the 'release_id' column
    df_sellers_aggregate['release_id'] = df_sellers_aggregate['release_url'].apply(extract_number)
    
    # Convert release_id to int for the merge
    df_sellers_aggregate['release_id'] = df_sellers_aggregate['release_id'].astype(int)
    
    # Load and read 'discogs_releases_dataset_light.csv'
    df_discogs = pd.read_csv('discogs_releases_dataset_light.csv')
    
    # Format release_date
    df_discogs.release_date = df_discogs.release_date.astype(str)
    df_discogs.release_date = df_discogs.release_date.str[:-2]
    
    # Merge df_sellers_aggregate with df_discogs
    df_sellers_aggregate = df_sellers_aggregate.merge(df_discogs, how='inner', on='release_id')
    
    # Reorder the columns
    columns_ordered=['seller',
     'release_id',
     'release_url',
     'format',
     'format_detail',
     'genre',
     'style',
     'country',
     'release_date', 
     'media_condition',
     'sleeve_condition',
     'price',
     'nb_for_sale',
     'current_lowest_price',
     'have',
     'want',
     'avg_rating',
     'ratings',
     'low_price',
     'median_price',
     'high_price',
     'last_sold_date',
     'img_url',]
    
    df_sellers_aggregate = df_sellers_aggregate[columns_ordered]
    
    # Export the file as csv
    df_sellers_aggregate.to_csv('sellers_aggregate.csv', index=False)

except:
    print('Something went wrong')

else:
    print('sellers_aggregate.csv was successfully created')

