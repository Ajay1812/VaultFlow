import random
from faker import Faker

class LocationGenerator:
    def __init__(self):
            self.fake = Faker('en_IN')
    
    def generate(self):
        return {
            'city': self.fake.city(),
            'state': self.fake.state(),
            'region': random.choice(['North', 'South', 'East', 'West']),
            'pincode': self.fake.postcode()
        }

    def generate_batch(self, count):
        return [self.generate() for _ in range(count)]