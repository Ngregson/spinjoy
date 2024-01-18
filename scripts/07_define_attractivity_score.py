#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
from datetime import datetime
import glob

spinjoy_path = '/Users/nicolaslewagon/spinjoy/'
files = glob.glob(f'{spinjoy_path}aggregated_files/sellers_aggregate_*.csv')

# Select the string not containing 'scored'
files_not_scored = [f for f in files if 'scored' not in f]

# Read 'sellers_aggregate.csv'
df = pd.read_csv(f'{files_not_scored[0]}', parse_dates=['last_sold_date'])

# Create "date_diff"
df['date_diff'] = (datetime.today() - df.last_sold_date).dt.days

# Create "trending_release"
df['trending_release_score'] = None
df.loc[(df.nb_for_sale > 5) & (df.price > df.median_price) & (df.date_diff < 90), 'trending_release_score'] = 0.4

# Create "quality_score"
df['quality_score'] = None
df.loc[df.media_condition == 'Mint ', 'quality_score'] = 1
df.loc[df.media_condition == 'Near Mint ', 'quality_score'] = 0.9
df.loc[df.media_condition == 'Very Good Plus ', 'quality_score'] = 0.8
df.loc[df.media_condition == 'Very Good ', 'quality_score'] = 0.7

# Create "never_sold_score"
df['never_sold_score'] = None
df.loc[(df.last_sold_date.isna() == True) & (df.nb_for_sale > 1), 'never_sold_score'] = -1

# Create "not_selling_score"
df['not_selling_score'] = None
df.loc[(df.nb_for_sale > 10) & (df.date_diff > df.date_diff.mean()), 'not_selling_score'] = -0.5

# Create "rating_score"
df['rate_score'] = df['avg_rating']/5

# Create "popularity_score"
df['popularity_score'] = df['want']/(df['have']+df['want'])

# Create "attractivity_score"
scores = ['trending_release_score','quality_score','not_selling_score','rate_score','popularity_score']
df['attractivity_score'] = df[scores].sum(axis=1)

# Define columns to write
columns_to_write = [
 'title',
 'artist_name',
 'format_detail',
 'genre',
 'style',
 'country',
 'release_date',
 'attractivity_score',
 'release_url']

#Get the current date
current_date = datetime.now().date()

# Get the current time
current_time = datetime.now().time().strftime("%Hh%M")

df.to_csv(f'{spinjoy_path}aggregated_files/sellers_aggregate_scored_{current_date}_{current_time}.csv', columns=columns_to_write, index=False)

