#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import math
import re
from datetime import datetime
import time
import sys
import pandas as pd

# Define the function with sellers as a parameter. "sellers" is a list.
def scrap_releases_url(sellers):

    # Create Chrome WebDriver with ad-blocking optionsx
    chrome_options = Options()
    chrome_options.add_extension('uBlock_Origin_extension_folder/1.54.0_0.crx')

    # Create an instance of the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    list = []
    
    for seller in sellers:
        
        # Construct url
        url = f'https://www.discogs.com/seller/{seller}/profile'

        # Get the URL
        driver.get(url)

        # Reject cookies
        try:
            reject_cookie = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))
            )
            reject_cookie.click()
        except TimeoutException:
            pass

        # Calculate the number of pages to scrap with 250 items per page
        raw_pagination = driver.find_element(By.XPATH,'//*[@id="pjax_container"]/nav[1]/form/strong').text
        match = re.search(r'\d{1,3}(?:,\d{3})*(?=\D*$)', raw_pagination)
        nb_for_sale = int(match.group().replace(',', ''))
        max_page = math.ceil(nb_for_sale/250)

        for page in range(max_page):

            if page <max_page:
                url_page = f'{url}?sort=listed%2Cdesc&limit=250&page={page+1}'
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
                    
                list.append([seller, release_url, media_condition, sleeve_condition, price])

    
    driver.quit()
    # Create a dataframe
    df = pd.DataFrame(list, columns = ['seller','release_url','media_condition','sleeve_condition','price'])

    # Remove the duplicates
    df.drop_duplicates(inplace=True)

    # Get the current date
    current_date = datetime.now().date()

    # Get the current time
    current_time = datetime.now().time().strftime("%Hh%M")

    #Get the names of the sellers a string
    result_string = '_'.join(sellers)

    df.to_csv(f'releases_urls/releases_urls_{result_string}_{current_date}_{current_time}.csv', index=False)

if __name__ == "__main__":
    # Check if command-line arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python scrap_releases_url.py <list_elements>")
        sys.exit(1)

    # The list provided as command-line arguments
    my_list = sys.argv[1:]

    # Call the function with the list provided as command-line arguments
    scrap_releases_url(my_list)
    

