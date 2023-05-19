import os
import time
import pandas as pd
import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def setup_driver(download_directory, path_to_chromedriver):
    """Set up the WebDriver."""
    # Initialize Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    })
    service = Service(path_to_chromedriver)
    # Initialize WebDriver with the designated ChromeDriver path and options
    try:
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Failed to set up WebDriver: {e}")
        return None

def login_to_website(driver, url, login_username_selector, login_password_selector, login_button_selector, username, password):
    """Log into the website."""
    try:
        driver.get(url)
        username_input = driver.find_element(By.CSS_SELECTOR, login_username_selector)
        password_input = driver.find_element(By.CSS_SELECTOR, login_password_selector)
        # Fill the login form and submit
        username_input.send_keys(username)
        password_input.send_keys(password)
        driver.find_element(By.CSS_SELECTOR, login_button_selector).click()
    except Exception as e:
        print(f"Failed to login: {e}")

def navigate_to_exports(driver, drop_down_selector, submenu_selector, link_text):
    """Navigate to exports."""
    try:
        time.sleep(5)
        # Open the drop down menu
        driver.find_element(By.CSS_SELECTOR, drop_down_selector).click()
        time.sleep(5)
        # Open the sub-menu
        driver.find_element(By.CSS_SELECTOR, submenu_selector).click()
        wait = WebDriverWait(driver, 10)
        # Wait for the link to be clickable and click on it
        pending_shipments_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
        pending_shipments_link.click()
        time.sleep(5)
    except Exception as e:
        print(f"Failed to navigate to exports: {e}")

def export_to_csv(driver, export_link_text):
    """Export to CSV."""
    try:
        # Find the CSV export link and click on it
        driver.find_element(By.LINK_TEXT, export_link_text).click()
        time.sleep(5)
        driver.quit()
    except Exception as e:
        print(f"Failed to export to CSV: {e}")

def process_csv_file(download_directory, csv_filename, filter_conditions, sort_column):
    """Process the CSV file."""
    try:
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(os.path.join(download_directory, csv_filename))
        # Filter the data according to the given conditions
        for column, condition in filter_conditions.items():
            data = data[condition(data[column])]
        # Sort the data by the designated column
        data = data.sort_values(by=sort_column)
        # Save the processed data to a new CSV file
        data.to_csv(os.path.join(download_directory, "processed_data.csv"), index=False)
        # Remove the original downloaded CSV file
        os.remove(os.path.join(download_directory, csv_filename))
    except Exception as e:
        print(f"Failed to process CSV file: {e}")

def process_shipments(url, username, password, download_directory, path_to_chromedriver,
                      login_username_selector, login_password_selector, login_button_selector,
                      drop_down_selector, submenu_selector, link_text,
                      export_link_text, csv_filename, filter_conditions, sort_column):
    """Process the shipments."""
    driver = setup_driver(download_directory, path_to_chromedriver)
    if driver is not None:
        login_to_website(driver, url, login_username_selector, login_password_selector, login_button_selector, username, password)
        navigate_to_exports(driver, drop_down_selector, submenu_selector, link_text)
        export_to_csv(driver, export_link_text)
        process_csv_file(download_directory, csv_filename, filter_conditions, sort_column)

# Schedule the process_shipments function to run at 8 am, 12 pm, and 4 pm (16:00) *24 hour clock
schedule.every().day.at("08:00").do(process_shipments, url, username, password, download_directory, path_to_chromedriver,
                      login_username_selector, login_password_selector, login_button_selector, 
                      drop_down_selector, submenu_selector, link_text,
                      export_link_text, csv_filename, filter_conditions, sort_column)
schedule.every().day.at("12:00").do(process_shipments, url, username, password, download_directory, path_to_chromedriver,
                      login_username_selector, login_password_selector, login_button_selector, 
                      drop_down_selector, submenu_selector, link_text,
                      export_link_text, csv_filename, filter_conditions, sort_column)
schedule.every().day.at("16:00").do(process_shipments, url, username, password, download_directory, path_to_chromedriver,
                      login_username_selector, login_password_selector, login_button_selector, 
                      drop_down_selector, submenu_selector, link_text,
                      export_link_text, csv_filename, filter_conditions, sort_column)

# Run the scheduler in a loop
while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print(f"An error occurred during scheduled tasks: {e}")
        break  # Or: continue, if you want the loop to keep running even if one task fails
    time.sleep(1)

