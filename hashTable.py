#ZyBook C949 Figure 15.2.1: Hash table with chaining: Each bucket contains a list of items.

class HashMap:
    def __init__(self, initial_capacity=20):
        # Initialize the hash map with a specified or default capacity
        self.capacity = initial_capacity
        # Create buckets, each initialized as an empty list
        self.buckets = [[] for _ in range(initial_capacity)]

    def insert(self, key, item):
        # Calculate the hash to determine the bucket index
        bucket = hash(key) % self.capacity
        # Retrieve the bucket list for the given key
        bucket_list = self.buckets[bucket]

        for i, (existing_key, existing_item) in enumerate(bucket_list):
            # Check if the key already exists in the bucket
            if existing_key == key:
                # Update the existing key with the new item
                bucket_list[i] = (key, item)
                return True

        # If key not found, insert a new key-value pair into the bucket
        bucket_list.append((key, item))
        return True

    def lookup(self, key):
        # Calculate the hash to determine the bucket index
        bucket = hash(key) % self.capacity
        # Retrieve the bucket list for the given key
        for existing_key, existing_item in self.buckets[bucket]:
            if existing_key == key:
                return existing_item
        return None

    def hash_remove(self, key):
        # Calculate the hash to determine the bucket index
        bucket = hash(key) % self.capacity
        # Retrieve the bucket list for the given key
        bucket_list = self.buckets[bucket]

        for i, (existing_key, _) in enumerate(bucket_list):
            if existing_key == key:
                # Remove the key-value pair from the bucket
                del bucket_list[i]
                return True

        print(f"Key '{key}' not found in the hash map.")
        return False  # Key not found
