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
    """
    Set up the WebDriver.
    :param download_directory: The directory where files will be downloaded.
    :param path_to_chromedriver: The path to the ChromeDriver executable.
    :return: A WebDriver instance.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    })
    service = Service(path_to_chromedriver)
    try:
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Failed to set up WebDriver: {e}")
        return None

def login_to_website(driver, url, login_username_selector, login_password_selector, login_button_selector, username, password):
    """
    Log into the website.
    :param driver: The WebDriver instance.
    :param url: The URL of the website.
    :param login_username_selector: The CSS selector for the username input field.
    :param login_password_selector: The CSS selector for the password input field.
    :param login_button_selector: The CSS selector for the login button.
    :param username: The username.
    :param password: The password.
    """
    try:
        driver.get(url)
        username_input = driver.find_element(By.CSS_SELECTOR, login_username_selector)
        password_input = driver.find_element(By.CSS_SELECTOR, login_password_selector)
        username_input.send_keys(username)
        password_input.send_keys(password)
        driver.find_element(By.CSS_SELECTOR, login_button_selector).click()
    except Exception as e:
        print(f"Failed to login: {e}")

def navigate_to_exports(driver, drop_down_selector, submenu_selector, link_text):
    """
    Navigate to the exports section.
    :param driver: The WebDriver instance.
    :param drop_down_selector: The CSS selector for the drop-down menu.
    :param submenu_selector: The CSS selector for the sub-menu.
    :param link_text: The text of the link to click on.
    """
    try:
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, drop_down_selector).click()
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, submenu_selector).click()
        wait = WebDriverWait(driver, 10)
        pending_shipments_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
        pending_shipments_link.click()
        time.sleep(5)
    except Exception as e:
        print(f"Failed to navigate to exports: {e}")

def export_to_csv(driver, export_link_text):
    """
    Export data to a CSV file.
    :param driver: The WebDriver instance.
    :param export_link_text: The text of the link for exporting data.
    """
    try:
        driver.find_element(By.LINK_TEXT, export_link_text).click()
        time.sleep(5)
    except Exception as e:
        print(f"Failed to export to CSV: {e}")
    finally:
        driver.quit()

def process_csv_file(download_directory, csv_filename, filter_conditions, sort_column):
    """
    Process the downloaded CSV file.
    :param download_directory: The directory where the CSV file was downloaded.
    :param csv_filename: The name of the CSV file.
    :param filter_conditions: The conditions to filter the data.
    :param sort_column: The column to sort the data by.
    """
    try:
        data = pd.read_csv(os.path.join(download_directory, csv_filename))
        for column, condition in filter_conditions.items():
            data = data[condition(data[column])]
        data = data.sort_values(by=sort_column)
        data.to_csv(os.path.join(download_directory, "processed_data.csv"), index=False)
        os.remove(os.path.join(download_directory, csv_filename))
    except Exception as e:
        print(f"Failed to process CSV file: {e}")

def process_shipments(url, username, password, download_directory, path_to_chromedriver,
                      login_username_selector, login_password_selector, login_button_selector,
                      drop_down_selector, submenu_selector, link_text,
                      export_link_text, csv_filename, filter_conditions, sort_column):
    """
    Process the shipments.
    :param url: The URL of the website.
    :param username: The username for login.
    :param password: The password for login.
    :param download_directory: The directory where files will be downloaded.
    :param path_to_chromedriver: The path to the ChromeDriver executable.
    :param login_username_selector: The CSS selector for the username input field.
    :param login_password_selector: The CSS selector for the password input field.
    :param login_button_selector: The CSS selector for the login button.
    :param drop_down_selector: The CSS selector for the drop-down menu.
    :param submenu_selector: The CSS selector for the sub-menu.
    :param link_text: The text of the link to click on.
    :param export_link_text: The text of the link for exporting data.
    :param csv_filename: The name of the CSV file.
    :param filter_conditions: The conditions to filter the data.
    :param sort_column: The column to sort the data by.
    """
    driver = setup_driver(download_directory, path_to_chromedriver)
    if driver is not None:
        login_to_website(driver, url, login_username_selector, login_password_selector, login_button_selector, username, password)
        navigate_to_exports(driver, drop_down_selector, submenu_selector, link_text)
        export_to_csv(driver, export_link_text)
        process_csv_file(download_directory, csv_filename, filter_conditions, sort_column)

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

