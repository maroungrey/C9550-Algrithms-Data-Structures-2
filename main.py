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
    print(f"Package ID: {loaded_package.package_id}, Address: {loaded_package.address}")