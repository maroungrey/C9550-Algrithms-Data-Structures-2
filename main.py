# Student ID: 010309427
# Maroun Barqawi
# C950 Data Structures And Algorithms 2


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

for row in distance_data:
    print(row["Address"])

# Create trucks
# truck1 = Truck(truck_id=1)
# truck2 = Truck(truck_id=2)
# truck3 = Truck(truck_id=3)

# Create a hash map to store packages
package_hash_map = HashMap()

# Insert packages into the hash map using package IDs as keys
for package in packages:
    package_hash_map.insert(package.package_id, package)

package14 = package_hash_map.lookup(14)
truck1 = Truck(1) 
truck1.load_package(package14)


package14 = package_hash_map.lookup(14) 
print(f"Package 14 address: {package14.address}")
print(f"Package 14 statuses: {package14.status_updates}")

# Manually determine which packages go into which truck
assigned_packages = {
    # truck1: [15, 22, 24, 3, 14, 19, 16, 13, 20, 36, 38, 21, 37, 35, 39, 40],
    # truck2: [1, 2, 4, 5, 7, 10, 11, 12, 17, 18, 23, 27, 29, 30, 33, 34],
    # truck3: [6, 9, 25, 26, 28, 32, 8, 31],
    # truck1: [14, 15],
    # truck2: [33, 2],
    # truck3: [26, 25],
}

# Load packages into assigned trucks
for truck, package_ids in assigned_packages.items():
    for package_id in package_ids:
        package = package_hash_map.lookup(package_id)
        if package:
            truck.load_package(package)

# Print information about loaded packages in each truck
print("\nTruck 1 loaded packages at 8:35 AM. ID:", end=" ")
for loaded_package in truck1.packages:
    print(f"{loaded_package.package_id}", end=" ")


# print("\nTruck 2 loaded packages at 9:35 AM. ID:", end=" ")
# for loaded_package in truck2.packages:
#     print(f"{loaded_package.package_id}", end=" ")


# print("\nTruck 3 loaded packages at 12:35 PM. ID:", end=" ")
# for loaded_package in truck3.packages:
#     print(f"{loaded_package.package_id}", end=" ")


# Extract the hub address from the first row of distance_data
HUB_ADDRESS = distance_data[0]['Address']
all_trucks_distance = 0
print()

def extract_route_addresses(truck, distance_data):

    addresses = []
    
    if len(truck.packages) > 0:
        addresses.append(truck.packages[0].address)

    route_addresses = [HUB_ADDRESS] + addresses
    print(f"Route addresses: {route_addresses}")
        
    return route_addresses

extract_route_addresses(truck1, distance_data)

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
        distance_key = '4001 South 700 East'
        hub_distance_key = '4001 South 700 East'
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

def send_truck_on_route(truck1, distance_data):
    # Get the route addresses dynamically
    print("Generating route")
    route_addresses = extract_route_addresses(truck1, distance_data)
    print(route_addresses)


    # Initialize current time and total distance
    # current_time = truck1.time_left_hub
    current_time = datetime.strptime('8:00', '%H:%M') 
    truck1.time_left_hub = current_time

    total_distance = 0

    def print_delivery_info(package_ids, start_address, end_address, distance, delivery_time):
        if package_ids:
            package_ids_str = ', '.join(str(pkg_id) for pkg_id in package_ids)
            print(f"Package ID: {package_ids_str}, Distance from {start_address} to {end_address}: {distance} miles, Estimated Delivery Time: {delivery_time.strftime('%I:%M %p')}")
        else:
            print(f"Finished Delivery. Distance from {start_address} to {end_address}: {distance} miles, Estimated Arrival Time: {delivery_time.strftime('%I:%M %p')}")

    # Print the time when the truck starts driving
    print(f"\nTruck {truck1.truck_id} starts driving at: {current_time.strftime('%I:%M %p')}")

    # Iterate through the route starting from the second address
    for i in range(1, len(route_addresses)):
        start_address = route_addresses[i - 1]
        end_address = route_addresses[i]

        if "end_address" in locals():

            # Print address and packages
            packages_at_address = [pkg for pkg in truck1.packages if pkg.address == end_address]


            # Get all packages with the current address
            # packages_at_address = [pkg for pkg in truck.packages if pkg.address == end_address]
            package_ids = [package.package_id for package in packages_at_address]


            if len(packages_at_address) > 0:

                # Get the distance from the CSV data
                distance = get_distance_from_csv(start_address, end_address, distance_data)

                # Calculate the estimated travel time based on the truck speed (18 miles per hour)
                travel_time_hours = distance / 18

                # Calculate the estimated delivery time for the current package
                delivery_time = current_time + timedelta(hours=travel_time_hours)

                if end_address:
                    truck1.update_current_location(end_address)
                    current_time = delivery_time

                # Update Delivery status
                for package in packages_at_address:
                    package.update_status("Delivered", delivery_time)


                # Print the distance and estimated delivery time
                print_delivery_info(package_ids, start_address, end_address, distance, delivery_time)

                # Update the total distance
                total_distance += distance

                # Update the current location and time of the truck
                truck1.update_current_location(end_address)
                current_time = delivery_time

                # Update the current location and time of the truck
                truck1.update_current_location(end_address)
                current_time = delivery_time


    # Print total distance from the last location back to the hub
    last_location_to_hub_distance = get_distance_to_or_from_hub(route_addresses[-1], distance_data, to_hub=False)
    last_location_to_hub_travel_time = last_location_to_hub_distance / 18
    last_location_to_hub_delivery_time = current_time + timedelta(hours=last_location_to_hub_travel_time)
    total_distance += last_location_to_hub_distance
    
    global all_trucks_distance 
    all_trucks_distance += total_distance
    
    print_delivery_info(None, route_addresses[-1], HUB_ADDRESS, last_location_to_hub_distance, last_location_to_hub_delivery_time)
    print(f"Total Distance Traveled: {total_distance:.1f} miles")

    return last_location_to_hub_delivery_time

send_truck_on_route(truck1, distance_data)

# Specify the departure time
departure_time_truck1 = datetime.strptime('08:35', '%H:%M')
# departure_time_truck2 = datetime.strptime('09:35', '%H:%M')

# # Set the departure time
# truck1.set_time_left_hub(departure_time_truck1)
# # truck2.set_time_left_hub(departure_time_truck2)

# # Send trucks on their routes
# for truck in [truck1, truck2]:
#     print()
#     # for package in truck.packages:
#         # package.update_status("En route", truck.time_left_hub)
#     print(f"\nTruck {truck.truck_id}")
#     last_delivery_time = send_truck_on_route(truck, distance_data)
#     print(f"Truck {truck.truck_id} returned to Hub at: {last_delivery_time.strftime('%I:%M %p')}")

# # Set the departure time for truck3 based on the last delivery time
# # truck3.set_time_left_hub(last_delivery_time)

# # Send truck3 on its route
# print()
# print(f"\nTruck {truck3.truck_id}")
# last_delivery_time_truck3 = send_truck_on_route(truck3, distance_data)
# print(f"Truck {truck3.truck_id} returned to Hub at: {last_delivery_time_truck3.strftime('%I:%M %p')}")

# # Total Distance
# print(f"\nTotal Distance for all trucks: {all_trucks_distance:.1f} miles.")


# # Update en route status
# for truck in [truck1, truck2, truck3]:
#     for package in truck.packages:
#         package.update_status("En route", truck.time_left_hub)

# Print status of the packages
print()
print("\nTimestamps of the packages:")
# Sort and print
# all_packages = truck1.packages + truck2.packages + truck3.packages
all_packages = truck1.packages
all_packages.sort(key=lambda x: x.package_id) 

for package in all_packages:

    output = f"Package {package.package_id}:  "
    
    output += "8:00 AM At hub  "
    
    for status, time in reversed(package.status_updates):
     
        if time is None: 
            time_str = "N/A"
        else:
            time_str = datetime.strftime(time, '%I:%M %p')

        status_string = f"{time_str} {status}"
        output += status_string + "  "
    
    print(output)