from datetime import date, timedelta
from dotenv import load_dotenv
from faker import Faker
import psycopg2
import os
import logging
import random
load_dotenv()

class Connection:
    def __init__(self, logger):
        self.logger = logger

    def connect(self):
        try:
            self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD')
        )
            self.logger.log_info(f'Connected to {self.conn}')
            return self.conn
        except psycopg2.OperationalError as e:
            self.logger.log_error('Connection', e) 
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.logger.log_info('Connection is closed')

class Logger:
    def __init__(self):
        logging.basicConfig(
            filename='logs/app.log',
            format='%(asctime)s %(levelname)s: %(message)s',
            level=logging.INFO,
            force=True
        )
        logging.getLogger('faker').setLevel(logging.ERROR)
        self.logger = logging.getLogger(__name__)
        
    def log_info(self, message):
        self.logger.info(message)
    
    def log_success(self, table_name, rows):
        self.logger.info(f'{table_name} → {rows} rows inserted')
        
    def log_error(self, table_name, error):
        self.logger.error(f'{table_name} → {error}')
        
class GenerateRecords:
    def __init__(self):
        self.fake = Faker('en_IN')
    
    def generate_location(self):
        return {
            'city': self.fake.city(),
            'state': self.fake.state(),
            'region': random.choice(['North', 'South', 'East', 'West']),
            'pincode': self.fake.postcode()
        }
    def generate_dates(self):
        start = date(2023, 1, 1)
        random_date = start + timedelta(days=random.randint(0, 364))
        return {
            'full_date': random_date,
            'day': random_date.day,
            'month': random_date.month,
            'month_name': random_date.strftime('%B'),
            'quarter': (random_date.month - 1) // 3 + 1,
            'year': random_date.year
        }
    def generate_products(self):
        products = [
            ('iPhone 14', 'Electronics', 'Smartphones', 'Apple', 79999),
            ('Samsung TV', 'Electronics', 'Televisions', 'Samsung', 55000),
            ('Nike Shoes', 'Clothing', 'Footwear', 'Nike', 8999),
            ('Macbook M1 Air', 'Electronics', 'Laptops', 'Apple', 65999),
            ('Macbook M2 Pro', 'Electronics', 'Laptops', 'Apple', 149999),
            ('Adidas Shoes', 'Clothing', 'Footwear', 'Adidas', 9999),
            ('Nvidia RTX 5090 Ti', 'Electronics', 'PC', 'Nvidia', 659999),
        ]
        p = random.choice(products)
        return {
            'name': p[0],
            'category': p[1],
            'sub_category': p[2],
            'brand': p[3],
            'unit_price': p[4]
        }
    
    def generate_customer(self, location_id):
        return {
            'name': self.fake.name(),
            'age': random.randint(16, 80),
            'phone': self.fake.phone_number(),
            'email': self.fake.email(),
            'segment': random.choice(['Retail', 'Wholesale', 'Online']),
            'location_id': location_id
        }
    def generate_fact_orders(self, customer_id, date_id, product_id, location_id, unit_price):
        qty = random.randint(1, 5)
        discount = random.choice([0, 5, 10, 15, 20])
        total_amount = unit_price * qty * (1 - discount/100)
        return {
            'customer_id': customer_id,
            'date_id': date_id,
            'product_id': product_id,
            'location_id': location_id,
            'unit_price': unit_price,
            'qty': qty,
            'discount': discount,
            'total_amount': total_amount,
            'status': random.choice(['Delivered', 'Returned', 'Pending'])
        }

class LoadTables:
    def __init__(self, conn, logger):
        self.conn = conn
        self.logger = logger
    
    def load(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data)) 
        values = list(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        # print(f'SQL: {sql}')
        # print(f'Values: {values}')
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            returned_id = cur.fetchone()[0]
            self.conn.commit()
            self.logger.log_success(table, 1)
            return returned_id
        except Exception as e:
            self.conn.rollback()
            self.logger.log_error(table, e)
            # print(f'ERROR: {e}') 

class Pipeline:
    def __init__(self):
        self.logger = Logger()
        self.conn_obj = Connection(self.logger)
        self.conn = self.conn_obj.connect()
        print(f'Connection: {self.conn}')
        self.gen = GenerateRecords()
        self.loader = LoadTables(self.conn, self.logger)
        
    def run(self, records=100):
        for i in range(records):
            # Step 1: insert location → get location_id
            location_data = self.gen.generate_location()
            location_id = self.loader.load('dim_locations', location_data)
            print(location_id)
            # Step 2: insert date → get date_id
            date_data = self.gen.generate_dates()
            date_id = self.loader.load('dim_dates', date_data)
            print(date_id)
            # Step 3: insert product → get product_id + unit_price
            product_data = self.gen.generate_products()
            product_id = self.loader.load('dim_products', product_data)
            print(product_id)
            # Step 4: insert customer with location_id → get customer_id
            customer_data = self.gen.generate_customer(location_id=location_id)
            customer_id = self.loader.load('dim_customers', customer_data)
            print(customer_id)
            # Step 5: insert order with all IDs
            order_data = self.gen.generate_fact_orders(customer_id=customer_id, date_id=date_id,location_id=location_id, product_id=product_id,unit_price=product_data['unit_price'])
            order_id = self.loader.load('fact_orders', order_data)
            print(order_id)
        # Step 6: disconnect
        self.conn_obj.disconnect()

if __name__ == '__main__':
    A = Pipeline()
    A.run(records=10)