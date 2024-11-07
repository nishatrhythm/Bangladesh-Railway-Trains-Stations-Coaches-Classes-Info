from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import itertools
import os
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Path to chromedriver
service = Service('C:\\WebDriver\\chromedriver.exe')

# Define output file
output_file = "station_list_dest_to.txt"

# Clear the output file if it already contains text
if os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        pass  # Overwrite the file with nothing to clear it
    print(Fore.YELLOW + f"Cleared the contents of {output_file}.")

# Initialize the WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Function to write unique stations to the file
def write_station_to_file(station_name):
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(station_name + "\n")

# Function to sort the file contents alphabetically
def sort_file_contents(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        sorted_stations = sorted(file.readlines())
    with open(file_path, 'w', encoding="utf-8") as file:
        file.writelines(sorted_stations)
    print(Fore.BLUE + f"Sorted station names in {file_path}.")

# Open the website and interact with the page
try:
    # Step 1: Navigate to the URL
    driver.get('https://eticket.railway.gov.bd/')
    print(Fore.GREEN + "Navigated to the homepage.")

    # Wait until the page URL is fully loaded before proceeding
    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print(Fore.GREEN + "Page fully loaded.")

    # Wait 2 seconds after the page has fully loaded
    time.sleep(2)

    # Step 2: Wait until the "I AGREE" button is visible and clickable after full load
    try:
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'I AGREE')]"))
        )
        agree_button.click()
        print(Fore.GREEN + "Clicked on 'I AGREE' button.")
    except TimeoutException:
        print(Fore.RED + "The 'I AGREE' button was not found or did not appear in time.")

    # Step 3: Click on 'From' input field to ensure 'To' input field is visible
    from_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'dest_from'))
    )
    from_input.click()
    print(Fore.GREEN + "Clicked on 'From' station input field to make 'To' input field visible.")

    # Step 4: Prepare 'To' input field for search
    from_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'dest_to'))
    )
    from_input.click()
    print(Fore.GREEN + "Located and clicked on 'To' station input field.")

    # Step 5: Generate all two-letter combinations and combinations with a space
    seen_stations = set()  # Track unique station names to avoid duplicates
    combinations = list(itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=2)) + \
                   [(char + ' ') for char in "abcdefghijklmnopqrstuvwxyz"]

    for entry in combinations:
        query = ''.join(entry) if isinstance(entry, tuple) else entry
        from_input.clear()
        from_input.send_keys(query)
        time.sleep(0.5)  # Shorter wait to capture instant responses

        # Fetch and process station suggestions
        try:
            station_elements = driver.find_elements(By.XPATH, "//ul[@id='ui-id-2']/li/a")
            if station_elements:
                for station in station_elements:
                    station_name = station.text.strip()
                    if station_name and station_name not in seen_stations:
                        print(Fore.GREEN + f"Found station: {station_name}")
                        write_station_to_file(station_name)
                        seen_stations.add(station_name)
        except (TimeoutException, NoSuchElementException):
            print(Fore.RED + f"No stations found for query '{query}'")

finally:
    driver.quit()
    print(Fore.YELLOW + "Browser closed and script completed.")

    # Sort the contents of the file before exiting the script
    sort_file_contents(output_file)