class Package:
    def __init__(self, package_id, address, city, zip_code, weight, special_note=None):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.special_note = special_note
        self.delivery_time = None