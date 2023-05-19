import os
import time
import pandas as pd
import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def process_shipments(url, username, password, download_directory, path_to_chromedriver,
                      login_username_selector, login_password_selector, login_button_selector, 
                      drop_down_selector, submenu_selector, link_text,
                      export_link_text, csv_filename, filter_conditions, sort_column):
    
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()

    # Define Chrome preferences
    chrome_options.add_experimental_option("prefs", {
        # Set the default directory for downloaded files
        "download.default_directory": download_directory,

        # Disable the prompt that asks for download confirmation
        "download.prompt_for_download": False,

        # Instruct Chrome to use the new download directory instead of the default one
        "download.directory_upgrade": True
    })

    # Define the ChromeDriver service
    service = Service(path_to_chromedriver)

    # Start the WebDriver with the specified options
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to the specified URL
    driver.get(url)

    # Log in with credentials
    username_input = driver.find_element(By.CSS_SELECTOR, login_username_selector)
    password_input = driver.find_element(By.CSS_SELECTOR, login_password_selector)
    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element(By.CSS_SELECTOR, login_button_selector).click()

    # Wait for the new page to load
    time.sleep(5)

    # Click on the dropdown menu
    driver.find_element(By.CSS_SELECTOR, drop_down_selector).click()
    time.sleep(5)

    # Click on the submenu
    driver.find_element(By.CSS_SELECTOR, submenu_selector).click()
    wait = WebDriverWait(driver, 10)
    pending_shipments_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
    pending_shipments_link.click()

    # Wait for the new page to load
    time.sleep(5)

    # Click on "Export to CSV"
    driver.find_element(By.LINK_TEXT, export_link_text).click()
    time.sleep(5)
    driver.quit()

    # Read the downloaded CSV file
    data = pd.read_csv(os.path.join(download_directory, csv_filename))

    # Apply the filters to the data, and save the results to a new variable.
    # filter_conditions is a dictionary with column name as key and conditions as values
    for column, condition in filter_conditions.items():
        data = data[condition(data[column])]

    # Sort by given column
    data = data.sort_values(by=sort_column)

    # Save the new CSV file
    data.to_csv(os.path.join(download_directory, "extracted_data.csv"), index=False)

    # Delete the original CSV file
    os.remove(os.path.join(download_directory, csv_filename))

# Add your arguments here
url = "https://your_website.com"
username = "your_username"
password = "your_password"
download_directory = r"path_to_your_directory"
path_to_chromedriver = r'path_to_chromedriver.exe' 
login_username_selector = "CSS_SELECTOR_TO_USERNAME_FIELD"
login_password_selector = "CSS_SELECTOR_TO_PASSWORD_FIELD"
login_button_selector = "CSS_SELECTOR_TO_LOGIN_BUTTON"
drop_down_selector = "CSS_SELECTOR_TO_DROPDOWN"
submenu_selector = "CSS_SELECTOR_TO_SUBMENU"
link_text = "LINK_TEXT_TO_NAVIGATE_TO"
export_link_text = "LINK_TEXT_TO_EXPORT_TO_CSV"
csv_filename = "csv_file_to_be_processed.csv"

# Update this dictionary as per your filter conditions.
# The keys are column names and the values are lambda functions that describe the filter condition
filter_conditions = {
    'ColumnName1': lambda x: (x == "---"),
    'ColumnName2': lambda x: (~x.str.startswith("UNK") & x.notna()),
    # Add more filters as needed
}

sort_column = 'ColumnNameToSortBy'  # The name of the column by which to sort the data

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
    schedule.run_pending()
    time.sleep(1)
