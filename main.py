from datetime import datetime, timedelta
from package import Package
from truck import Truck
from csvReader import CSVReader
from hashTable import HashMap
import logging

# Load packages from the Package file
package_file_path = 'CSV/Package.csv'
packages = CSVReader.read_packages(package_file_path)

# Load distance information from the Distance file
distance_file_path = 'CSV/Distance.csv'
distance_data = CSVReader.read_distance(distance_file_path)

# Create trucks
truck1 = Truck(truck_id=1)
truck2 = Truck(truck_id=2)
truck3 = Truck(truck_id=3)

# Create two drivers
driver1 = "Driver 1"
driver2 = "Driver 2"

# Assign trucks to drivers
driver1_trucks = [truck1, truck3]
driver2_trucks = [truck2]

# Create a hash map to store packages
package_hash_map = HashMap()

# Insert packages into the hash map using package IDs as keys
for package in packages:
    package_hash_map.insert(package.package_id, package)

# Manually determine which packages go into which truck
assigned_package_ids = [15, 22, 24]
for package_id in assigned_package_ids:
    package = package_hash_map.lookup(package_id)
    if package:
        truck2.load_package(package)

# Specify the departure time
departure_time = datetime.strptime('08:00', '%H:%M')

# Set the departure time
truck1.set_time_left_hub(departure_time)
truck2.set_time_left_hub(departure_time)

# Print information about loaded packages in each truck
print("Truck 1 loaded packages:")
for loaded_package in truck1.packages:
    print(f"Package ID: {loaded_package.package_id}, Address: {loaded_package.address}")

print("Truck 2 loaded packages:")
for loaded_package in truck2.packages:
    print(f"Package ID: {loaded_package.package_id}, Address: {loaded_package.address}")

print("Truck 3 loaded packages:")
for loaded_package in truck3.packages:
    print(f"Package ID: {loaded_package.package_id}, Address: {loaded_package.address}")


# Extract the hub address from the first row of distance_data
HUB_ADDRESS = distance_data[0]['Address']


def extract_route_addresses(truck, distance_data):
    # Extract unique addresses from loaded packages
    addresses = set(package.address for package in truck.packages)
    
    # Add the hub address as the starting point if it's not already in the set
    if HUB_ADDRESS not in addresses:
        addresses.add(HUB_ADDRESS)
    
    # Convert set to a list and sort it for the route
    route_addresses = sorted(list(addresses), key=lambda x: x != HUB_ADDRESS)
    
    return route_addresses



def get_distance_from_csv(start_address, end_address, distance_data):
    try:
        # Find the row for the start_address
        start_row = next(row for row in distance_data if row['Address'] == start_address)

        # Check if the end_address is present in the headers
        available_headers = distance_data[0].keys()
        if end_address not in available_headers:
            print(f"Error: Column header not found for {end_address}. Available headers: {available_headers}")
            return None

        # Get the distance from the corresponding cell and convert it to a float
        distance = float(start_row[end_address])

        return distance
    except StopIteration:
        print(f"Error: No data found for {start_address} to {end_address}")
        return None
    except KeyError:
        print(f"Error: Column header not found for {end_address}")
        return None
    except ValueError:
        print(f"Error: Distance value is not a valid number for {start_address} to {end_address}")
        return None

def get_distance_to_or_from_hub(address, distance_data, to_hub=True):
    try:
        # Find the row for the given address
        row = next(row for row in distance_data if row['Address'] == address)

        # Get the distance to or from the hub and convert it to a float
        distance_key = '4001 South 700 East'  # Adjust this based on the actual header for hub distances
        hub_distance_key = '4001 South 700 East'  # Adjust this based on the actual header for hub distances
        distance = float(row[hub_distance_key]) if to_hub else float(row[distance_key])

        return distance
    except StopIteration:
        print(f"Error: No data found for {address}")
        return None
    except KeyError:
        print(f"Error: Column header not found for {address}")
        return None
    except ValueError:
        print(f"Error: Distance value is not a valid number for {address}")
        return None

    




def send_truck_on_route(truck, distance_data):
    # Get the route addresses dynamically
    route_addresses = extract_route_addresses(truck, distance_data)

    # Initialize current time based on the departure time
    current_time = truck.time_left_hub

    # Iterate through the route starting from the second address
    for i in range(1, len(route_addresses)):
        start_address = route_addresses[i - 1]
        end_address = route_addresses[i]

        # Get the package ID for the current address
        package_id = None
        for package in truck.packages:
            if package.address == end_address:
                package_id = package.package_id  # Replace 'package_id' with your actual attribute name
                break

        # Get the distance from the CSV data
        distance = get_distance_from_csv(start_address, end_address, distance_data)

        # Calculate the estimated travel time based on the truck speed (18 miles per hour)
        travel_time_hours = distance / 18

        # Calculate the estimated delivery time for the current package
        delivery_time = current_time + timedelta(hours=travel_time_hours)

        # Print the distance and estimated delivery time
        print(f"Package ID: {package_id}, Distance from {start_address} to {end_address}: {distance} miles, Estimated Delivery Time: {delivery_time.strftime('%I:%M %p')}")

        # Update the current location and time of the truck
        truck.update_current_location(end_address)
        current_time = delivery_time

    # Print distance from the last location back to the hub
    last_location_to_hub_distance = get_distance_to_or_from_hub(route_addresses[-1], distance_data, to_hub=False)
    last_location_to_hub_travel_time = last_location_to_hub_distance / 18
    last_location_to_hub_delivery_time = current_time + timedelta(hours=last_location_to_hub_travel_time)
    print(f"Distance from {route_addresses[-1]} to WGU {HUB_ADDRESS}: {last_location_to_hub_distance} miles, Arrival Time: {last_location_to_hub_delivery_time.strftime('%I:%M %p')}")

# Example of sending truck2 on its route
print("\nDistance & Arrival Time:")
send_truck_on_route(truck2, distance_data)