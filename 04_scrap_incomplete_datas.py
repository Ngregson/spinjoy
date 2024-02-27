#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import pandas as pd
import glob

# Use glob to get the file path matching the pattern
file_path = glob.glob('/Users/nicolaslewagon/spinjoy/releases_urls/releases_urls_*.csv')[0]

#Extract seller(s) name(s)
parts = file_path.split('_')
sellers = "_".join(parts[3:-2])

df_master = pd.read_csv(file_path)

# Set the maximum number of rows per DataFrame
max_rows_per_df = 20

# Calculate the number of DataFrames needed
num_dataframes = len(df_master) // max_rows_per_df + 1

# Split the DataFrame into chunks
dataframes_list = [df_master.iloc[i*max_rows_per_df:(i+1)*max_rows_per_df].copy() for i in range(num_dataframes)]

# Print the number of resulting DataFrames
print(f"Number of DataFrames: {len(dataframes_list)}")

# Create Chrome WebDriver with ad-blocking optionsx
chrome_options = Options()
chrome_options.add_extension('/Users/nicolaslewagon/spinjoy/scripts/uBlock_Origin_extension_folder/1.54.0_0.crx')

for i, df in enumerate(dataframes_list):

    # Create an instance of the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://www.discogs.com/release/28813273-Jungkook-Golden')

    # Reject cookies
    try:
        reject_cookie = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))
        )
        reject_cookie.click()
    except TimeoutException:
        pass

    # List of new columns to retrieve
    new_columns = ['have', 'want', 'avg_rating', 'ratings', 'last_sold_date', 'low_price', 'median_price', 'high_price']

    # Initialize columns with None
    for column in new_columns:
        df.loc[:, column] = None

    # Loop through each URL in the 'release_url' column
    for index, row in df.iterrows():
        release_url = row['release_url']

        try:
            # Perform actions with Selenium on each URL
            driver.get(release_url)
    
            # Wait for "Statistics" block to ensure it has loaded
            try:
                WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.ID, 'release-stats'))
                )
    
                # Get the statistic information
                df.loc[index, 'have'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[1]/a').text
                df.loc[index, 'want'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[2]/a').text
                df.loc[index, 'avg_rating'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[3]/span[2]').text
                df.loc[index, 'ratings'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[4]/a').text
                
                try:
                    df.loc[index, 'last_sold_date'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[1]/a/time').text
                except:
                    df.loc[index, 'last_sold_date'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[1]/span[2]').text
                    
                df.loc[index, 'low_price'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[2]/span[2]').text
                df.loc[index, 'median_price'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[3]/span[2]').text
                df.loc[index, 'high_price'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[4]/span[2]').text
            
            except TimeoutException:      
                columns_statistics = ['have','want', 'avg_rating', 'ratings', 'last_sold_date', 'low_price', 'median_price', 'high_price']
                for column_statistics in columns_statistics:
                    df[column_statistics] = None
                    
        except TimeoutException:
            pass

    driver.quit()

    # Get the current date
    current_date = datetime.now().date()

    # Get the current time
    current_time = datetime.now().time().strftime("%Hh%M")
        
    # Export the dataframe
    try:
        df.to_csv(f'/Users/nicolaslewagon/spinjoy/csv_files/datas_discogs_{sellers}_part_{i + 1}_{current_date}_{current_time}_full.csv', index=False)
    except:
        print("Something went wrong")
    else:
        print(f'datas_discogs_{sellers}_part_{i + 1}_{current_date}_{current_time}_full.csv has been created')

