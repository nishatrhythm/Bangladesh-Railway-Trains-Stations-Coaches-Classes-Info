import json
import os
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Directory containing processed JSON files
processed_directory = 'processed'

# Function to create an index of JSON files by origin and destination
def create_index(directory):
    index = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if 'origin_city_name' in data and 'destination_city_name' in data:
                    key = (data['origin_city_name'].lower(), data['destination_city_name'].lower())
                    index[key] = file_path
    return index

# Function to search for and display fare data using the index
def search_and_display_fares(index, origin, destination):
    search_key = (origin.lower(), destination.lower())
    if search_key in index:
        file_path = index[search_key]
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"\n{Fore.CYAN}Fare list for {Fore.GREEN}{origin.title()}{Fore.CYAN} to {Fore.GREEN}{destination.title()}:\n")
            table_data = []
            for info in data['info']:
                total_fare = info['fare'] + info['vat_amount']
                table_data.append([
                    f"{Fore.YELLOW}{info['type']}{Style.RESET_ALL}",
                    f"{Fore.GREEN}{info['fare']:.2f}{Style.RESET_ALL}",
                    f"{Fore.MAGENTA}{info['vat_amount']:.2f}{Style.RESET_ALL}",
                    f"{Fore.CYAN}{total_fare:.2f}{Style.RESET_ALL}"
                ])

            # Display the table
            headers = [
                f"{Fore.LIGHTBLUE_EX}Seat Type{Style.RESET_ALL}",
                f"{Fore.LIGHTBLUE_EX}Base Fare{Style.RESET_ALL}",
                f"{Fore.LIGHTBLUE_EX}VAT Amount (15%){Style.RESET_ALL}",
                f"{Fore.LIGHTBLUE_EX}Total Fare{Style.RESET_ALL}"
            ]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

            # Add notes below the table
            print(f"\n{Fore.YELLOW}Note: {Style.RESET_ALL}An extra {Fore.LIGHTBLUE_EX}BDT 20{Style.RESET_ALL} online payment charge applies. Also, total fare includes {Fore.LIGHTBLUE_EX}BDT 50{Style.RESET_ALL} Bedding Charges per seat for {Fore.YELLOW}AC_B{Style.RESET_ALL} and {Fore.YELLOW}F_BERTH{Style.RESET_ALL} seat classes.\n")

    else:
        print(f"{Fore.RED}No data found for {origin.title()} to {destination.title()} or the stations may not have central server connection for online ticket management.")

# Function to display the menu and handle user choices
def display_menu():
    print(f"\n{Fore.LIGHTBLUE_EX}Select an option:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Search for fare{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Exit{Style.RESET_ALL}")
    choice = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}").strip()
    return choice

# Main function to drive the menu-based system
def main():
    # Create the index
    # print(f"{Fore.LIGHTBLUE_EX}Creating index for faster search...{Style.RESET_ALL}")
    index = create_index(processed_directory)
    # print(f"{Fore.GREEN}Index created successfully!{Style.RESET_ALL}")

    while True:
        # Display menu and get user choice
        choice = display_menu()
        
        if choice == '1':
            # Get origin and destination from user
            origin = input(f"{Fore.LIGHTBLUE_EX}Enter the origin station: {Style.RESET_ALL}").strip()
            destination = input(f"{Fore.LIGHTBLUE_EX}Enter the destination station: {Style.RESET_ALL}").strip()
            # Search and display fare information
            search_and_display_fares(index, origin, destination)
        
        elif choice == '2':
            print(f"{Fore.GREEN}Exiting the script. Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

# Run the main function
if __name__ == "__main__":
    main()