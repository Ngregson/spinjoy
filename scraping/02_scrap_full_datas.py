#!/usr/bin/env python
# coding: utf-8

# In[86]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
#import time
import pandas as pd
import glob

# Use glob to get the file path matching the pattern
file_path = glob.glob('releases_urls/releases_urls_*.csv')[0]

df_master = pd.read_csv(file_path)

# Set the maximum number of rows per DataFrame
max_rows_per_df = 1000

# Calculate the number of DataFrames needed
num_dataframes = len(df_master) // max_rows_per_df + 1

# Split the DataFrame into chunks
dataframes_list = [df_master.iloc[i*max_rows_per_df:(i+1)*max_rows_per_df].copy() for i in range(num_dataframes)]

# Print the number of resulting DataFrames
print(f"Number of DataFrames: {len(dataframes_list)}")

# Create Chrome WebDriver with ad-blocking optionsx
chrome_options = Options()
chrome_options.add_extension('uBlock_Origin_extension_folder/1.54.0_0.crx')

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
    new_columns = ['img_url', 'format_detail', 'nb_for_sale', 'current_lowest_price', 'have', 'want', 'avg_rating', 'ratings', 'last_sold_date', 'low_price', 'median_price', 'high_price']

    # Initialize columns with None
    for column in new_columns:
        df.loc[:, column] = None

    # Loop through each URL in the 'release_url' column
    for index, row in df.iterrows():
        release_url = row['release_url']

        try:
            # Perform actions with Selenium on each URL
            driver.get(release_url)
    
            # Wait for the first block element in the right top corner to ensure it has loaded
            try:
                WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'body_32Bo9'))
                )
    
                # Store the retrieved information in the appropriated columns
                try:
                    df.loc[index, 'img_url'] = driver.find_element(By.XPATH, './/div[@class="image_3rzgk bezel_2NSgk"]/picture/img').get_attribute('src')
                except NoSuchElementException:
                    df.loc[index, 'img_url'] = None
                try:
                    df.loc[index, 'format_detail'] = driver.find_element(By.CLASS_NAME,'format_item_3SAJn').text
                except NoSuchElementException:
                    df.loc[index, 'format_detail'] = None
            except TimeoutException:
                df.loc[index, 'img_url'] = None
                df.loc[index, 'format_detail'] = None
    
    
            # Wait for the "For Sale on Discogs" block to ensure it has loaded
            try:
                WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'forsale_QoVFl'))
                )
    
                # Get infos
                try:
                    df.loc[index, 'nb_for_sale'] = driver.find_element(By.XPATH, './/span[@class="forsale_QoVFl"]/a').text
                except NoSuchElementException:
                    df.loc[index, 'nb_for_sale'] = None
                try:
                    df.loc[index, 'current_lowest_price'] = driver.find_element(By.CLASS_NAME, 'price_2Wkos').text
                except NoSuchElementException:
                    df.loc[index, 'current_lowest_price'] = None
            except TimeoutException:
                df.loc[index, 'nb_for_sale'] = None
                df.loc[index, 'current_lowest_price'] = None
    
    
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
        df.to_csv(f'csv_files/datas_discogs_part_{i + 1}_{current_date}_{current_time}_full.csv', index=False)
    except:
        print("Something went wrong")
    else:
        print(f'datas_discogs_part_{i + 1}_{current_date}_{current_time}_full.csv has been created')
        

