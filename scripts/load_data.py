from datetime import date, timedelta
from dotenv import load_dotenv
from faker import Faker
import psycopg2
import os
import logging
import random

load_dotenv()

class Logger:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)

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


class Connection:
    def __init__(self, logger):
        self.logger = logger
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            self.logger.log_info(f'Connected to DB: {os.getenv("DB_NAME")}')
            return self.conn
        except psycopg2.OperationalError as e:
            self.logger.log_error('Connection', e)
            raise Exception("Database connection failed")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.logger.log_info('Connection closed')


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
        total_amount = unit_price * qty * (1 - discount / 100)
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
        if not conn:
            raise Exception("No DB connection passed to loader")
        self.conn = conn
        self.logger = logger

    def load(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"

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
            raise


class Pipeline:
    def __init__(self):
        self.logger = Logger()
        self.conn_obj = Connection(self.logger)
        self.conn = self.conn_obj.connect()

        if not self.conn:
            raise Exception("Connection failed")

        self.gen = GenerateRecords()
        self.loader = LoadTables(self.conn, self.logger)

    def run(self, records=100):
        location_ids = []
        for _ in range(10):
            lid = self.loader.load('dim_locations', self.gen.generate_location())
            location_ids.append(lid)

        product_ids = {}
        for _ in range(7):
            data = self.gen.generate_products()
            pid = self.loader.load('dim_products', data)
            product_ids[pid] = data['unit_price']

        date_ids = []
        for _ in range(50):
            did = self.loader.load('dim_dates', self.gen.generate_dates())
            date_ids.append(did)

        customer_ids = []
        for _ in range(50):
            cid = self.loader.load(
                'dim_customers',
                self.gen.generate_customer(random.choice(location_ids))
            )
            customer_ids.append(cid)

        for _ in range(records):
            pid = random.choice(list(product_ids.keys()))
            print('Product ID: ', pid)
            self.loader.load(
                'fact_orders',
                self.gen.generate_fact_orders(
                    customer_id=random.choice(customer_ids),
                    date_id=random.choice(date_ids),
                    product_id=pid,
                    location_id=random.choice(location_ids),
                    unit_price=product_ids[pid]
                )
            )

        self.conn_obj.disconnect()


# if __name__ == '__main__':
#     pipeline = Pipeline()
#     pipeline.run(records=100)