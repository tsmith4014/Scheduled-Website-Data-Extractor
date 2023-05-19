# Web Automation Script for Scheduled Exports

This repository contains a Python script that uses Selenium WebDriver for automated website navigation and interaction. It's designed to log in to a website, navigate to a specific section, download a CSV file, process that CSV file, and schedule these tasks to run at specified times.

A dummy HTML file, for a fictitious shipping company, is provided as an example of the structure the script is designed to interact with.

## Prerequisites

- Python 3.x
- Selenium
- pandas
- schedule
- Google Chrome Browser
- ChromeDriver

## Installation

1. Clone this repository.
2. Install the necessary Python libraries using pip and the provided requirements.txt file:
  pip install -r requirements.txt
3. Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/) and place it in a known location on your system.

## Usage

1. Open the Python script in your favorite editor.
2. Replace the placeholders in the `process_shipments` function call with actual values suitable for your use case.
3. Save the Python script.

To use the provided dummy HTML file as a reference:

1. Open `dummy.html` in your web browser.
2. Open the Python script in your favorite editor.
3. Modify the `process_shipments` function call as follows:

 ```python
 # Define your URL and login credentials
 url = "path_to_your_local_html_file"  # replace with actual local html file path
 username = "test_username"  # replace with actual username
 password = "test_password"  # replace with actual password

 # Define the directory where you want to download the CSV file
 # and the path to the chromedriver executable
 download_directory = r"C:\path_to_directory"
 path_to_chromedriver = r'C:\path_to_chromedriver.exe'  # change this to your actual path

 # Define CSS selectors for username, password, and login button
 login_username_selector = "#username"  # replace with actual CSS selector
 login_password_selector = "#password"  # replace with actual CSS selector
 login_button_selector = "#login-button"  # replace with actual CSS selector

 # Define CSS selectors for navigating to the CSV file
 drop_down_selector = "#dropdown"  # replace with actual CSS selector
 submenu_selector = "#submenu"  # replace with actual CSS selector
 link_text = "Exports"  # replace with actual link text

 # Define the link text for exporting to CSV
 export_link_text = "Export to CSV"  # replace with actual link text
 ```
4. Save the Python script and run it.

## Note

Please note that this script is for illustrative purposes only. It is important to respect the terms of service of any website you interact with. Always obtain necessary permissions before scraping a website. Respect privacy and confidentiality when handling collected data.

## License

MIT License.

Modify the content as you see fit. Remember to replace the placeholders (like "path_to_your_local_html_file") with actual paths relevant to your project.


