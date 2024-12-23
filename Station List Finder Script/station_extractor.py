import json, os

script_dir = os.path.dirname(__file__)
input_file = os.path.join(script_dir, "local_storage_handshake_data.json")

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

cities = data.get("cities", [])

from_cities = []
to_cities = []

for city in cities:
    city_name = city.get("city_name", "")
    if city.get("is_enable_for_from") == 1:
        from_cities.append(city_name)
    to_cities.append(city_name)

with open(os.path.join(script_dir, "station_list_dest_from.txt"), "w", encoding="utf-8") as from_file:
    from_file.write("\n".join(from_cities))

with open(os.path.join(script_dir, "station_list_dest_to.txt"), "w", encoding="utf-8") as to_file:
    to_file.write("\n".join(to_cities))

print("Files 'station_list_dest_from.txt' and 'station_list_dest_to.txt' created successfully!")