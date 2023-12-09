from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id, capacity=16):
        self.truck_id = truck_id
        self.capacity = capacity
        self.packages = []
        self.time_left_hub = None
        self.path = []

    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            return True
        return False

    def unload_all_packages(self):
        unloaded_packages = self.packages
        self.packages = []
        return unloaded_packages

    def set_time_left_hub(self, departure_time):
        self.time_left_hub = departure_time

    def set_path(self, addresses):
        self.path = addresses

    def deliver_packages(self):
        delivery_time = self.time_left_hub
        for package in self.packages:
            delivery_time += timedelta(minutes=15)  # Assuming 15 minutes for each delivery
            package.delivery_time = delivery_time
        self.time_left_hub = delivery_time  # Update truck's time