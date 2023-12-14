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

# Create trucks
truck1 = Truck(truck_id=1)
truck2 = Truck(truck_id=2)
truck3 = Truck(truck_id=3)

# Create a hash map to store packages
package_hash_map = HashMap()

# Insert packages into the hash map using package IDs as keys
for package in packages:
    package_hash_map.insert(package.package_id, package)

# Manually determine which packages go into which truck
assigned_packages = {
    truck1: [15, 22, 24, 3, 14, 19, 16, 13, 20, 36, 38, 21, 37, 35, 39, 40],
    truck2: [1, 2, 4, 5, 7, 10, 11, 12, 17, 18, 23, 27, 29, 30, 33, 34],
    truck3: [6, 9, 25, 26, 28, 32, 8, 31],
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


print("\nTruck 2 loaded packages at 9:35 AM. ID:", end=" ")
for loaded_package in truck2.packages:
    print(f"{loaded_package.package_id}", end=" ")


print("\nTruck 3 loaded packages at 12:35 PM. ID:", end=" ")
for loaded_package in truck3.packages:
    print(f"{loaded_package.package_id}", end=" ")


# Extract the hub address from the first row of distance_data
HUB_ADDRESS = distance_data[0]['Address']
all_trucks_distance = 0
print()

def extract_route_addresses(truck, distance_data):
    addresses = set(package.address for package in truck.packages)
    current_address = HUB_ADDRESS
    route_addresses = [current_address]
    remaining_addresses = set(addresses)

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

def send_truck_on_route(truck, distance_data):

    # Get the route addresses dynamically
    route_addresses = extract_route_addresses(truck, distance_data)

    current_time = truck.time_left_hub
    total_distance = 0

    def print_delivery_info(package_ids, start_address, end_address, distance, delivery_time):
        if distance > 0:
            if package_ids:
                package_ids_str = ', '.join(str(pkg_id) for pkg_id in package_ids)
                print(f"Package ID: {package_ids_str}, Distance from {start_address} to {end_address}: {distance} miles, Estimated Delivery Time: {delivery_time.strftime('%I:%M %p')}")
            else:
                print(f"Finished Delivery. Distance from {start_address} to {end_address}: {distance} miles, Estimated Arrival Time: {delivery_time.strftime('%I:%M %p')}")

    print(f"\nTruck {truck.truck_id} starts driving at: {current_time.strftime('%I:%M %p')}")

    for i in range(1, len(route_addresses)):
        start_address = route_addresses[i - 1]
        end_address = route_addresses[i]

        packages_at_address = [pkg for pkg in truck.packages if pkg.address == end_address]
        package_ids = [package.package_id for package in packages_at_address]

        distance = get_distance_from_csv(start_address, end_address, distance_data)
        travel_time_hours = distance / 18
        delivery_time = current_time + timedelta(hours=travel_time_hours)

        for package in packages_at_address:
            package.update_status("Delivered", delivery_time)

        print_delivery_info(package_ids, start_address, end_address, distance, delivery_time)
        total_distance += distance

        truck.update_current_location(end_address)
        current_time = delivery_time

    last_location_to_hub_distance = get_distance_to_or_from_hub(route_addresses[-1], distance_data, to_hub=False)
    last_location_to_hub_travel_time = last_location_to_hub_distance / 18
    last_location_to_hub_delivery_time = current_time + timedelta(hours=last_location_to_hub_travel_time)
    total_distance += last_location_to_hub_distance
    
    global all_trucks_distance 
    all_trucks_distance += total_distance
    setattr(truck, 'all_trucks_distance', all_trucks_distance)

    print_delivery_info(None, route_addresses[-1], HUB_ADDRESS, last_location_to_hub_distance, last_location_to_hub_delivery_time)
    print(f"Total Distance Traveled: {total_distance:.1f} miles")

    return last_location_to_hub_delivery_time



# Specify the departure time
departure_time_truck1 = datetime.strptime('08:35', '%H:%M')
departure_time_truck2 = datetime.strptime('09:35', '%H:%M')

# Set departure times for all trucks
truck1.set_time_left_hub(departure_time_truck1)
truck2.set_time_left_hub(departure_time_truck2)

# Send trucks on their routes
for truck in [truck1, truck2]:
    print()
    print(f"\nTruck {truck.truck_id}")
    last_delivery_time = send_truck_on_route(truck, distance_data)
    print(f"Truck {truck.truck_id} returned to Hub at: {last_delivery_time.strftime('%I:%M %p')}")

# Set the departure time for truck3 based on the last delivery time
truck3.set_time_left_hub(last_delivery_time)

# Send truck3 on its route
print()
print(f"\nTruck {truck3.truck_id}")
last_delivery_time_truck3 = send_truck_on_route(truck3, distance_data)
print(f"Truck {truck3.truck_id} returned to Hub at: {last_delivery_time_truck3.strftime('%I:%M %p')}")
print()
print(f"\nTotal Distance for all trucks: {all_trucks_distance:.1f} miles.")



# Update en route status
for truck in [truck1, truck2, truck3]:
    for package in truck.packages:
        package.update_status("En route", truck.time_left_hub)


while True:
    print()
    print("------------------------------------------------")
    print()
    print("Select an option:")
    print()
    print("1. View status of specific package at given time") 
    print("2. View status of all packages at given time")
    print("3. View timestamps for all packages at all times")

    choice = input("\nEnter your choice 1, 2, 3 or quit to exit: ")
    all_packages = truck1.packages + truck2.packages + truck3.packages
    print()

    if choice.lower() == 'q' or choice.lower() == 'quit':
        print("Exited")
        break

    if choice == "1":

        while True:
                # Get package ID and time from user
                package_id = input("Enter package ID: ")
                input_time = input("Enter time in 24-hour format (for example: 8:20): ")
                
                try:
                    # Convert to datetime
                    input_time = datetime.strptime(input_time, '%H:%M')
                    break
                except ValueError:
                    print("Invalid time format. Please try again.")

        # Find package
        package = None
        for pkg in all_packages:
            if pkg.package_id == int(package_id):
                package = pkg
                break

        if package:
            # Get status at time
            status_at_time = package.initial_status  
            for status, update_time in package.status_updates:

                if update_time <= input_time:
                    # Set status
                    status_at_time = status

                # Convert input time to string
                input_time_str = input_time.isoformat()
                update_time_str = update_time.isoformat()

                if update_time_str <= input_time_str:
                    status_at_time = status

                # Break the loop if "Delivered" status is encountered
                if status == "Delivered":
                    break

            # Convert time to datetime object
            input_time_str = datetime.strftime(input_time,"%I:%M %p")        
            print(f"\nPackage ID: {package_id} status at {input_time_str}: {status_at_time}")
        
        else:
            print(f"Invalid package ID: {package_id}")

    elif choice == "2":

        while True:
            input_time = input("Enter time in 24-hour format (for example: 8:20): ")

            try: 
                input_time = datetime.strptime(input_time, '%H:%M')
                break
            except ValueError:
                print("Invalid time format. Please try again.")

        print(f"\nPackage statuses at {input_time:%I:%M %p}:")
        
        all_packages.sort(key=lambda x: x.package_id)

        for package in all_packages:

            truck = next((t for t in [truck1, truck2, truck3] if package in t.packages), None)
            if truck and truck.time_left_hub <= input_time:
                status_at_time = "En route"
            else:
                # original status logic
                status_at_time = package.initial_status  
                for status, update_time in package.status_updates:
                    if update_time <= input_time:
                        status_at_time = status
                    if status == "Delivered":
                        break

            print(f"Package ID {package.package_id}: {status_at_time}")

    elif choice == "3":
        # Print status of the packages
        print()
        print("\nTimestamps of the packages:")
        print()
        # Sort and print
        all_packages.sort(key=lambda x: x.package_id) 

        for package in all_packages:
            output = f"Package {package.package_id}:  "
            output += f"8:00 AM {package.initial_status}  "
            
            for status, time in reversed(package.status_updates):
                if time is None:
                    time_str = "N/A"
                else:
                    time_str = datetime.strftime(time, '%I:%M %p')

                status_string = f"{time_str} {status}"
                output += status_string + "  "

                # Break the loop if "Delivered" status is encountered
                if status == "Delivered":
                    break
            
            print(output)

    