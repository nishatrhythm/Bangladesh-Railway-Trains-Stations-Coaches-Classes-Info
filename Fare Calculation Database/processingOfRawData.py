import json
import os

# Directories for the two folders to compare
folder1 = '06-Feb-2025'
folder2 = '07-Feb-2025'
output_directory = 'processed'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to save JSON data to a file
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Function to extract and process relevant data from the JSON
def extract_relevant_data(data):
    if 'data' in data and 'trains' in data['data'] and data['data']['trains']:
        origin = data['data']['trains'][0]['origin_city_name']
        destination = data['data']['trains'][0]['destination_city_name']
        info_dict = {}

        # Loop through all trains to collect unique seat types
        for train in data['data']['trains']:
            for seat in train['seat_types']:
                if seat['type'] not in info_dict:
                    info_dict[seat['type']] = {
                        "type": seat['type'],
                        "fare": float(seat['fare']),
                        "vat_percent": seat['vat_percent'],
                        "vat_amount": seat['vat_amount']
                    }

        return {
            "origin_city_name": origin,
            "destination_city_name": destination,
            "info": list(info_dict.values())
        }
    return None

# Get the set of filenames in both folders
files_in_folder1 = set(f for f in os.listdir(folder1) if f.endswith('.json'))
files_in_folder2 = set(f for f in os.listdir(folder2) if f.endswith('.json'))

# Union of all filenames (to handle unique files)
all_files = files_in_folder1.union(files_in_folder2)

# Process each file in the combined set
for filename in all_files:
    path1 = os.path.join(folder1, filename)
    path2 = os.path.join(folder2, filename)
    output_path = os.path.join(output_directory, filename)

    if filename in files_in_folder1 and filename in files_in_folder2:
        # Load and process both files
        data1 = load_json(path1)
        data2 = load_json(path2)

        processed_data1 = extract_relevant_data(data1)
        processed_data2 = extract_relevant_data(data2)

        # Check if both have valid processed data
        if processed_data1 and processed_data2:
            if (processed_data1['origin_city_name'] == processed_data2['origin_city_name'] and
                processed_data1['destination_city_name'] == processed_data2['destination_city_name']):

                # Merge unique 'info' data based on 'type'
                info_dict = {entry['type']: entry for entry in processed_data1['info']}
                for entry in processed_data2['info']:
                    if entry['type'] not in info_dict:
                        info_dict[entry['type']] = entry

                combined_info = list(info_dict.values())
                combined_data = {
                    "origin_city_name": processed_data1['origin_city_name'],
                    "destination_city_name": processed_data1['destination_city_name'],
                    "info": combined_info
                }

                # Save the combined data
                save_json(combined_data, output_path)
                print(f"Combined and saved: {output_path}")

            else:
                # Save separately due to mismatch in origin/destination
                save_json(processed_data1, os.path.join(output_directory, f"{filename}_12-Nov-2024.json"))
                save_json(processed_data2, os.path.join(output_directory, f"{filename}_13-Nov-2024.json"))
                print(f"Saved separately due to origin/destination mismatch: {filename}")

    elif filename in files_in_folder1:
        # Process and save the unique file from folder1
        data1 = load_json(path1)
        processed_data1 = extract_relevant_data(data1)
        if processed_data1:
            save_json(processed_data1, output_path)
            print(f"Processed and saved from {folder1}: {output_path}")

    elif filename in files_in_folder2:
        # Process and save the unique file from folder2
        data2 = load_json(path2)
        processed_data2 = extract_relevant_data(data2)
        if processed_data2:
            save_json(processed_data2, output_path)
            print(f"Processed and saved from {folder2}: {output_path}")

print("All files have been processed and saved to the 'processed' directory.")