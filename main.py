from datetime import datetime, timedelta
from package import Package
from truck import Truck
from csvReader import CSVReader

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

# Manually determine which packages go into which truck
truck2.load_package(packages[14])  # Package 15
truck2.load_package(packages[23])  # Package 24
truck2.load_package(packages[21])  # Package 22

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
    print(f"Package ID: {loaded_package.package_id}, Address: {loaded_package.address}, Estimated Delivery Time: {loaded_package.delivery_time}")

print("\nTruck 3 loaded packages:")
for loaded_package in truck3.packages:
    print(f"Package ID: {loaded_package.package_id}, Address: {loaded_package.address}, Estimated Delivery Time: {loaded_package.delivery_time}")


# Extract the hub address from the first row of distance_data
HUB_ADDRESS = distance_data[1]['Address']

def extract_route_addresses(truck, distance_data):
    # Extract unique addresses from loaded packages
    addresses = set(package.address for package in truck.packages)
    
    # Extract the hub address from the first row of distance_data
    hub_address = distance_data[1]['Address']  # Assuming the 'Address' column contains hub addresses
    
    # Add the hub address as the starting point
    addresses.add(hub_address)
    
    # Convert set to a list and sort it for the route
    route_addresses = sorted(list(addresses), key=lambda x: x if x != hub_address else '')
    
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

        # Get the distance from the corresponding cell
        distance = start_row[end_address]

        return distance
    except StopIteration:
        print(f"Error: No data found for {start_address} to {end_address}")
        return None
    except KeyError:
        print(f"Error: Column header not found for {end_address}")
        return None

def get_distance_to_or_from_hub(address, distance_data, to_hub=True):
    try:
        # Find the row for the given address
        row = next(row for row in distance_data if row['Address'] == address)

        # Get the distance to or from the hub
        distance_key = '4001 South 700 East'  # Adjust this based on the actual header for hub distances
        if to_hub:
            return row[distance_key]
        else:
            return row[distance_key]
    except StopIteration:
        print(f"Error: No data found for {address}")
        return None
    except KeyError:
        print(f"Error: Column header not found for {address}")
        return None

def send_truck_on_route(truck, distance_data):
    # Get the route addresses dynamically
    route_addresses = extract_route_addresses(truck, distance_data)

    # Print distance from the hub to the first location
    hub_to_first_location_distance = get_distance_to_or_from_hub(route_addresses[0], distance_data)
    print(f"Distance from Hub to {route_addresses[0]}: {hub_to_first_location_distance} miles")

    # Iterate through the route
    for i in range(len(route_addresses) - 1):
        start_address = route_addresses[i]
        end_address = route_addresses[i + 1]

        # Get the distance from the CSV data
        distance = get_distance_from_csv(start_address, end_address, distance_data)

        # Print the distance
        print(f"Distance from {start_address} to {end_address}: {distance} miles")

        # Update the current location of the truck
        truck.update_current_location(end_address)

    # Print distance from the last location back to the hub
    last_location_to_hub_distance = get_distance_to_or_from_hub(route_addresses[-1], distance_data, to_hub=False)
    print(f"Distance from {route_addresses[-1]} to Hub: {last_location_to_hub_distance} miles")

# Example of sending truck2 on its route
send_truck_on_route(truck2, distance_data)