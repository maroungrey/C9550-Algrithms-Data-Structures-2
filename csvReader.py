import csv
from package import Package

class CSVReader:
    @staticmethod
    def read_packages(file_path):
        #Read package information from a CSV file and create Package objects.
        packages = []  # Initialize an empty list to store Package objects
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create a Package object for each row in the CSV file
                package = Package(
                    package_id=int(row['Package ID']),
                    address=row['Address'],
                    city=row['City'],
                    zip_code=row['Zip Code'],
                    weight=float(row['Weight']),
                    special_note=row['Special Note'] if 'Special Note' in row else None
                )
                packages.append(package) # Append the Package object to the list
        return packages
    
    @staticmethod
    def read_distance(file_path):
        distance_data = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                distance_data.append(row)
        return distance_data
