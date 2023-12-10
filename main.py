from datetime import datetime, timedelta
from package import Package
from truck import Truck
from csvReader import CSVReader
from hashTable import HashMap

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
assigned_packages = {
    truck1: [1, 2, 4, 5, 7, 10, 11, 12, 17, 18, 23, 27, 29, 30, 33, 34],
    truck2: [15, 22, 24, 3, 14, 19, 16, 13, 20, 36, 38, 21, 37, 35, 39, 40],
    truck3: [6, 9, 25, 26, 28, 32, 8, 31],
}

# Load packages into assigned trucks
for truck, package_ids in assigned_packages.items():
    for package_id in package_ids:
        package = package_hash_map.lookup(package_id)
        if package:
            truck.load_package(package)


def set_departure_and_get_arrival(truck, departure_time, distance_data):
    truck.set_time_left_hub(departure_time)
    finish_time = send_truck_on_route(truck, distance_data)
    return truck.time_left_hub, finish_time


# Print information about loaded packages in each truck
print()
print("Truck 1 loaded packages:", end=" ")
for loaded_package in truck1.packages:
    print(f"{loaded_package.package_id}", end=" ")
print()

print("Truck 2 loaded packages:", end=" ")
for loaded_package in truck2.packages:
    print(f"{loaded_package.package_id}", end=" ")
print()

print("Truck 3 loaded packages:", end=" ")
for loaded_package in truck3.packages:
    print(f"{loaded_package.package_id}", end=" ")
print()

# Extract the hub address from the first row of distance_data
HUB_ADDRESS = distance_data[0]['Address']


def extract_route_addresses(truck, distance_data):
    # Extract unique addresses from loaded packages
    addresses = set(package.address for package in truck.packages)

    # Add the hub address as the starting point if it's not already in the set
    if HUB_ADDRESS not in addresses:
        addresses.add(HUB_ADDRESS)

    # Convert set to a list
    addresses_list = list(addresses)

    # Find the optimal route using a greedy algorithm based on the Distance.csv file
    current_address = HUB_ADDRESS
    route_addresses = [current_address]
    remaining_addresses = set(addresses_list)

    while remaining_addresses:
        closest_address = min(remaining_addresses, key=lambda addr: get_distance_from_csv(current_address, addr, distance_data))
        route_addresses.append(closest_address)
        remaining_addresses.remove(closest_address)
        current_address = closest_address

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

    # Initialize current time and total distance
    current_time = truck.time_left_hub
    total_distance = 0

    def print_delivery_info(package_ids, start_address, end_address, distance, delivery_time):
        if package_ids:
            package_ids_str = ', '.join(str(pkg_id) for pkg_id in package_ids)
            print(f"Package ID: {package_ids_str}, Distance from {start_address} to {end_address}: {distance} miles, Estimated Delivery Time: {delivery_time.strftime('%I:%M %p')}")
        else:
            print(f"Package ID: None, Distance from {start_address} to {end_address}: {distance} miles, Estimated Delivery Time: {delivery_time.strftime('%I:%M %p')}")

    # Print the time when the truck starts driving
    print(f"\nTruck {truck.truck_id} starts driving at: {current_time.strftime('%I:%M %p')}")

    # Iterate through the route starting from the second address
    for i in range(1, len(route_addresses)):
        start_address = route_addresses[i - 1]
        end_address = route_addresses[i]

        # Get all packages with the current address
        packages_at_address = [pkg for pkg in truck.packages if pkg.address == end_address]
        package_ids = [package.package_id for package in packages_at_address]

        # Get the distance from the CSV data
        distance = get_distance_from_csv(start_address, end_address, distance_data)

        # Calculate the estimated travel time based on the truck speed (18 miles per hour)
        travel_time_hours = distance / 18

        # Calculate the estimated delivery time for the current package
        delivery_time = current_time + timedelta(hours=travel_time_hours)

        # Print the distance and estimated delivery time
        print_delivery_info(package_ids, start_address, end_address, distance, delivery_time)

        # Update the total distance
        total_distance += distance

        # Update the current location and time of the truck
        truck.update_current_location(end_address)
        current_time = delivery_time


    # Update the current location and time of the truck
    truck.update_current_location(end_address)
    current_time = delivery_time

    # Print total distance from the last location back to the hub
    last_location_to_hub_distance = get_distance_to_or_from_hub(route_addresses[-1], distance_data, to_hub=False)
    last_location_to_hub_travel_time = last_location_to_hub_distance / 18
    last_location_to_hub_delivery_time = current_time + timedelta(hours=last_location_to_hub_travel_time)
    total_distance += last_location_to_hub_distance

    print_delivery_info(None, route_addresses[-1], HUB_ADDRESS, last_location_to_hub_distance, last_location_to_hub_delivery_time)
    print(f"Total Distance Traveled: {total_distance:.1f} miles")

    return last_location_to_hub_delivery_time


# Specify the departure time
departure_time = datetime.strptime('08:00', '%H:%M')

# Set the departure time
truck1.set_time_left_hub(departure_time)
truck2.set_time_left_hub(departure_time)

# Send trucks on their routes
for truck in [truck1, truck2]:
    print(f"\nTruck {truck.truck_id} Distance & Arrival Time:")
    last_delivery_time = send_truck_on_route(truck, distance_data)
    print(f"Truck {truck.truck_id} returned to Hub at: {last_delivery_time.strftime('%I:%M %p')}")

# Set the departure time for truck3 based on the last delivery time
truck3.set_time_left_hub(last_delivery_time)

# Send truck3 on its route
print(f"\nTruck {truck3.truck_id} Distance & Arrival Time:")
last_delivery_time_truck3 = send_truck_on_route(truck3, distance_data)
# print(f"Last Location to Hub Delivery Time: {last_delivery_time_truck3.strftime('%I:%M %p')}")