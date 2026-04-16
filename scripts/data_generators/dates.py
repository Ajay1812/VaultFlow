from datetime import timedelta, date
import random

class DateGenerator:
    def __init__(self, start_year=2023, num_days=365):
        self.start_year = start_year
        self.start_date = date(start_year, 1, 1)
        self.num_days = num_days
        
    def generate(self):
        random_date = self.start_date + timedelta(
            days=random.randint(0, self.num_days - 1)
        )
        return {
            'full_date': random_date,
            'day': random_date.day,
            'month': random_date.month,
            'month_name': random_date.strftime('%B'),
            'quarter': (random_date.month - 1) // 3 + 1,
            'year': random_date.year
        }
        
    def generate_batch(self, count):
        return [self.generate() for _ in range(count)]