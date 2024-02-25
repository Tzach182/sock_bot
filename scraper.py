from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import numpy as np
import pandas as pd


def getTextFromSelector(driver, selector):
    """
    Retrieve the text content of an element identified by the CSS selector 'selector'.

    Args:
    - driver: WebDriver object (e.g., from Selenium)
    - selector: str, the CSS selector used to identify the element

    Returns:
    - str: The text content of the element identified by the selector.
           If the element is not found, returns numpy.nan.
    """
    element = None

    try:
        element = driver.find_element(By.CSS_SELECTOR, selector).text
    except (NoSuchElementException, WebDriverException) as error:
        print(error.msg)
        element = np.nan
    
    return element


def checkNextButtonExists(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, ".x-pagination .pagination__next")
    except NoSuchElementException:
        return False
    return True


def getInfo(driver):

    featuresList = ['condition','toeStyle','style','features','handmade','character','color','material',
                    'brand','occasion','sockLength','pattern','garmentCare','sizeType','theme']
    data = {}
    
    data['name'] = getTextFromSelector(driver, ".x-item-title__mainTitle > .ux-textspans")
    data['price'] = getTextFromSelector(driver, ".x-price-primary > .ux-textspans")
    for feature in featuresList:
        data[feature] = getTextFromSelector(driver, f".ux-labels-values--{feature} .ux-labels-values__values .ux-textspans")

    return data



# set options and base url and header names for dataframe
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options)
baseUrl='https://www.ebay.com/'
headerNames = ['name','price','condition','toeStyle','style','features','handmade','character',
               'color','material','brand','occasion','sockLength','pattern','garmentCare','sizeType','theme', 'availability']
firstTime = True


driver.get(baseUrl)
wait = WebDriverWait(driver, 5)
time.sleep(2)

# set search word
searchBox = driver.find_element("id", "gh-ac")
searchBox.send_keys("socks")
searchBox.send_keys(Keys.RETURN)
time.sleep(3)

# set variables for data, and the current window
original_window = driver.current_window_handle
assert len(driver.window_handles) == 1
data = {}

# start run
while(checkNextButtonExists(driver)):
    #print url in case the script breaks so you can continue from where it stopped
    print(driver.current_url)
    entries = driver.find_elements(By.CSS_SELECTOR,".srp-results > .s-item")

    # run through each search entry in the page
    for entry in entries:
        print(entries.index(entry))
        entry.click()
        try:
            wait.until(EC.number_of_windows_to_be(2))
        except TimeoutException as error:
            print(driver.current_url)
            print(error.msg)
            time.sleep(2)
            continue

        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        data = getInfo(driver)

        try:
            data["availability"] = driver.find_elements(By.CSS_SELECTOR, ".d-quantity__availability .ux-textspans")[2].text
        except (NoSuchElementException, WebDriverException, IndexError) as error:
            data["availability"] = np.nan
        
        output = pd.DataFrame() 
        df_dictionary = pd.DataFrame([data])
        output = pd.concat([output, df_dictionary], ignore_index=True)
        if(firstTime):
            output.to_csv("socks_database.csv", mode='a', index=False, header=headerNames)
            firstTime = False
        else:
            output.to_csv("socks_database.csv", mode='a', index=False, header=False)
            

        driver.close()
        time.sleep(2)
        driver.switch_to.window(original_window)
        time.sleep(2)
    

    nextButton = driver.find_element(By.CSS_SELECTOR, ".x-pagination .pagination__next")
    nextButton.click()


    time.sleep(2)
    # end of loop






driver.close()
