#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import glob
import sys
from datetime import datetime

files = glob.glob('/Users/nicolaslewagon/spinjoy/aggregated_files/sellers_aggregate_*.csv')

# Select the string containing 'scored'
files_scored = [f for f in files if 'scored' in f]

df = pd.read_csv(files_scored[0])

def define_spinjoy_selection(genres_nb,catalog_size):

    # Calculate the proportion of each genre in df 
    genres_proportion = df['genre'].value_counts(normalize=True)

    # Create a DataFrame with the first "genre_nb" rows
    df_genres = genres_proportion.head(genres_nb).reset_index()
    
    # Define new proportions of genres to apply to the Spinjoy (sj) Catalogue
    df_genres.proportion = df_genres.proportion / df_genres.proportion.sum()

    # New affectation for more clarity
    df_sj_genres = df_genres
    
    # Add a column for quantity per genre
    df_sj_genres["qty"] = (df_sj_genres["proportion"] * catalog_size).round(0).astype(int)
    
    #Create a container for the df_selected_genre that will be created in the loop
    dfs_selected_genre = []

    for n in df_sj_genres.index :

        mask_genre = df["genre"] == df_sj_genres.iloc[n,0]
        
        df_selected_genre = df[mask_genre].sort_values(by="attractivity_score",ascending=False).head(df_sj_genres.iloc[n,2])
        
        #subdf=pd.concat([subdf,df_loop])
        dfs_selected_genre.append(df_selected_genre)

    df_sj = pd.concat(dfs_selected_genre)

    #Get the current date
    current_date = datetime.now().date()

    # Get the current time
    current_time = datetime.now().time().strftime("%Hh%M")

    df_sj.to_csv(f'/Users/nicolaslewagon/spinjoy/spinjoy_catalog_{current_date}_{current_time}.csv')

