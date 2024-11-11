import json
import requests
import os
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize colorama
init(autoreset=True)

# Load stations from stations_en.json
with open('stations_en.json', 'r', encoding='utf-8') as file:
    stations_data = json.load(file)

stations = stations_data['stations']

# Date for the journey (change as needed)
date_of_journey = "13-Nov-2024"
seat_class = "S_CHAIR"

# Create a directory named with the date if it doesn't exist
output_directory = date_of_journey
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Log file to keep track of completed requests
log_file = os.path.join(output_directory, "completed_routes.log")

# Load completed routes from the log file
completed_routes = set()
if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        completed_routes = set(line.strip() for line in f)

# Function to log completed routes
def log_completed_route(from_city, to_city):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{from_city},{to_city}\n")

# Function to make a request and save the response
def fetch_and_save(from_city, to_city):
    # Skip if from_city and to_city are the same
    if from_city == to_city:
        return f"{Fore.YELLOW}Skipped: {from_city} to {to_city} (Same city)"
    
    # Check if this route has already been completed
    if f"{from_city},{to_city}" in completed_routes:
        return f"{Fore.CYAN}Already completed: {from_city} to {to_city}"

    # Request URL
    url = f"https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2?from_city={from_city}&to_city={to_city}&date_of_journey={date_of_journey}&seat_class={seat_class}"
    response = requests.get(url)
    
    if response.status_code == 200:
        response_data = response.json()
        
        if response_data['data']['trains']:
            # Save response data to file
            safe_from_city = from_city.replace(" ", "_")
            safe_to_city = to_city.replace(" ", "_")
            output_filename = os.path.join(output_directory, f"{safe_from_city}_{safe_to_city}.json")
            
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                json.dump(response_data, output_file, indent=4)
            
            # Log the completed route
            log_completed_route(from_city, to_city)
            return f"{Fore.GREEN}Saved: {output_filename}"
        else:
            # Log the completed route (no trains found)
            log_completed_route(from_city, to_city)
            return f"{Fore.YELLOW}Skipped: {from_city} to {to_city} (No trains found)"
    else:
        return f"{Fore.RED}Failed to fetch data for {from_city} to {to_city}. Status code: {response.status_code}"

# Run concurrent requests
with ThreadPoolExecutor(max_workers=20) as executor:
    future_to_trip = {
        executor.submit(fetch_and_save, from_city, to_city): (from_city, to_city)
        for from_city in stations
        for to_city in stations
    }
    
    for future in as_completed(future_to_trip):
        result = future.result()
        print(result)