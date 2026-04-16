from faker import Faker
import random

class CustomerGenerator:
    def __init__(self):
        self.fake = Faker('en_IN')
    
    def generate(self, location_id):
        return {
            'name': self.fake.name(),
            'age': random.randint(16, 80),
            'phone': self.fake.phone_number(),
            'email': self.fake.email(),
            'segment': random.choice(['Retail', 'Wholesale', 'Online']),
            'location_id': location_id
        }
    
    def generate_batch(self, count, location_ids):
        return [
            self.generate(location_id=random.choice(location_ids))
            for _ in range(count)
        ]