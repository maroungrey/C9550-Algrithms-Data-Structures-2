from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id, capacity=16):
        self.truck_id = truck_id
        self.capacity = capacity
        self.packages = []
        self.time_left_hub = None
        self.path = []
        self.current_location = None

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
    
    def set_time_arrived_to_hub(self, return_time):
        self.time_arrived_to_hub = return_time

    def set_path(self, addresses):
        self.path = addresses

    def update_current_location(self, new_location):
        self.current_location = new_location
