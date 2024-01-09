#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import math
import re
import time
import sys
import pandas as pd

def scrap_sellers_catalogues(list_urls):

    # Create Chrome WebDriver with ad-blocking optionsx
    chrome_options = Options()
    chrome_options.add_extension('uBlock_Origin_extension_folder/1.54.0_0.crx')

    # Create an instance of the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    for seller_url in list_urls:

        # Extract seller_name
        url_parts = seller_url.split('/')
        seller_index = url_parts.index('seller')
        seller_name = url_parts[seller_index + 1]

        # Get the URL
        driver.get(seller_url)

        # Reject cookies
        try:
            reject_cookie = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))
            )
            reject_cookie.click()
        except TimeoutException:
            print('No cookies banner')

        # Maximize the window
        #driver.maximize_window()

        # Calculate the number of pages to scrap with 250 items per page
        raw_pagination = driver.find_element(By.XPATH,'//*[@id="pjax_container"]/nav[1]/form/strong').text
        match = re.search(r'\d{1,3}(?:,\d{3})*(?=\D*$)', raw_pagination)
        nb_for_sale = int(match.group().replace(',', ''))
        max_page = math.ceil(nb_for_sale/250)

        items_list = []

        for page in range(max_page):

            if page <max_page:
                url_page = f'{seller_url}?sort=listed%2Cdesc&limit=250&page={page+1}'
                driver.get(url_page)

            else:
                break
    
            for i in range(250):

                try:

                    WebDriverWait(driver,3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'item_description'))
                    )
            
                    # Identify element with class='item_description' for the item i
                    item_description_element = driver.find_elements(By.CLASS_NAME, 'item_description')[i]

                    # Get the media condition
                    media_condition_element = item_description_element.find_element(By.XPATH, './/p[@class="item_condition"]/span[contains(@class, "condition-label-mobile")]/following-sibling::span')
                    media_condition = media_condition_element.text

                    # Get the sleeve condition
                    try:
                        sleeve_condition = item_description_element.find_element(By.CLASS_NAME, 'item_sleeve_condition').text
                    except NoSuchElementException:
                        sleeve_condition = None
            
                    # Get the 'view release' URL
                    view_release_link = item_description_element.find_element(By.CLASS_NAME, 'item_release_link')
                    release_url = view_release_link.get_attribute('href')

                    WebDriverWait(driver,3).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'price'))
                    )

                    # Identify the price with for the item i
                    item_price = driver.find_elements(By.CLASS_NAME, 'price')[i]
                    price = item_price.get_attribute('data-pricevalue')

                except IndexError:
                    break

                item_attributes = [release_url, media_condition, sleeve_condition, price]
                items_list.append(item_attributes)
        
        # Create a dataframe
        df_seller = pd.DataFrame(items_list, columns = ['release_url','media_condition','sleeve_condition','price'])

        # Stock the number of duplicates
        nb_of_duplicates = df_seller.duplicated().sum()

        # Remove the duplicates
        df_seller.drop_duplicates(inplace=True)

        # List of new columns to retrieve
        new_columns = ['img_url', 'format_detail', 'nb_for_sale', 'current_lowest_price', 'have',
              'want', 'avg_rating', 'ratings', 'last_sold_date', 'low_price', 'median_price', 'high_price']

        # Initialize columns with None
        for column in new_columns:
            df_seller[column] = None
    
        # Loop through each URL in the 'release_url' column
        for index, row in df_seller.iterrows():
            release_url = row['release_url']

            # Perform actions with Selenium on each URL
            driver.get(release_url)

            # Wait for the first block element in the right top corner to ensure it has loaded
            try:
                WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'body_32Bo9'))
                )

                # Store the retrieved information in the appropriated columns
                try:
                    df_seller.at[index, 'img_url'] = driver.find_element(By.XPATH, './/div[@class="image_3rzgk bezel_2NSgk"]/picture/img').get_attribute('src')
                except NoSuchElementException:
                    df_seller.at[index, 'img_url'] = None
                try:
                    df_seller.at[index, 'format_detail'] = driver.find_element(By.CLASS_NAME,'format_item_3SAJn').text
                except NoSuchElementException:
                    df_seller.at[index, 'format_detail'] = None
            except TimeoutException:
                df_seller.at[index, 'img_url'] = None
                df_seller.at[index, 'format_detail'] = None

            # Wait for the "For Sale on Discogs" block to ensure it has loaded
            try:
                WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'forsale_QoVFl'))
                )

                # Get infos
                try:
                    df_seller.at[index, 'nb_for_sale'] = driver.find_element(By.XPATH, './/span[@class="forsale_QoVFl"]/a').text
                except NoSuchElementException:
                    df_seller.at[index, 'nb_for_sale'] = None
                try:
                    df_seller.at[index, 'current_lowest_price'] = driver.find_element(By.CLASS_NAME, 'price_2Wkos').text
                except NoSuchElementException:
                    df_seller.at[index, 'current_lowest_price'] = None
            except TimeoutException:
                df_seller.at[index, 'nb_for_sale'] = None
                df_seller.at[index, 'current_lowest_price'] = None
        
            # Wait for "Statistics" block to ensure it has loaded
            try:
                WebDriverWait(driver,3).until(
                    EC.presence_of_element_located((By.ID, 'release-stats'))
                )

                # Get the statistic information
                df_seller.at[index, 'have'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[1]/a').text
                df_seller.at[index, 'want'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[2]/a').text
                df_seller.at[index, 'avg_rating'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[3]/span[2]').text
                df_seller.at[index, 'ratings'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[1]/li[4]/a').text
                try:
                    df_seller.at[index, 'last_sold_date'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[1]/a/time').text
                except:
                    df_seller.at[index, 'last_sold_date'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[1]/span[2]').text
                df_seller.at[index, 'low_price'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[2]/span[2]').text
                df_seller.at[index, 'median_price'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[3]/span[2]').text
                df_seller.at[index, 'high_price'] = driver.find_element(By.XPATH, '//*[@id="release-stats"]/div/div/ul[2]/li[4]/span[2]').text
            except TimeoutException:
                columns_statistics = ['have','want', 'avg_rating', 'ratings', 'last_sold_date', 'low_price', 'median_price', 'high_price']
                for column_statistics in columns_statistics:
                    df_seller[column_statistics] = None
        
        # Export the dataframe
        try:
            df_seller.to_csv(f'{seller_name}_full.csv', index=False)
        except:
            print("Something went wrong")
        else:
            print(f'{seller_name}_full.csv has been created after removing {nb_of_duplicates} duplicates')

    driver.quit()

if __name__ == "__main__":
    # Check if command-line arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python spinjoy_scraping.py <list_elements>")
        sys.exit(1)

    # The list provided as command-line arguments
    my_list = sys.argv[1:]

    # Call the function with the list provided as command-line arguments
    scrap_sellers_catalogues(my_list)

