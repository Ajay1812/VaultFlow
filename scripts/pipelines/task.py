from scripts.core.connection import Connection
from scripts.core.logger import Logger 
from scripts.data_generators.locations import LocationGenerator
from scripts.data_generators.dates import DateGenerator
from scripts.data_generators.products import ProductGenerator
from scripts.data_generators.customers import CustomerGenerator
from scripts.data_generators.orders import OrderGenerator
from scripts.loaders.location import LocationLoader
from scripts.loaders.date import DateLoader
from scripts.loaders.product import ProductLoader
from scripts.loaders.customer import CustomerLoader
from scripts.loaders.order import OrderLoader

def load_locations(count=5):
    logger = Logger()
    logger.info('load_locations')
    
    try:
        gen = LocationGenerator()
        conn = Connection(logger).connect() # db
        loader = LocationLoader(conn, logger)
        
        location_data = gen.generate_batch(count)
        location_ids = loader.load_batch(location_data)
        
        logger.info('load_locations')
        return location_ids  # XCom: passed to downstream tasks
    
    except Exception as e:
        logger.error('load_locations', e)
        raise
    
def load_dates(count=5):
    logger = Logger()
    logger.info('load_dates')\
    
    try:
        gen = DateGenerator()
        conn = Connection(logger).connect() # db
        loader = DateLoader(conn, logger)
        
        date_data = gen.generate_batch(count)
        date_ids = loader.load_batch(date_data)
        
        logger.info('load_dates')
        return date_ids  
    
    except Exception as e:
        logger.error('load_dates', e)
        raise
    
def load_products(count=5):
    logger = Logger()
    logger.info('load_products')\
    
    try:
        gen = ProductGenerator()
        conn = Connection(logger).connect() # db
        loader = ProductLoader(conn, logger)
        
        product_data = gen.generate_batch(count)
        product_ids = loader.load_batch(product_data)
        
        logger.info('load_products')
        return {
            pid: product_data[i]['unit_price']
            for i, pid in enumerate(product_ids)
        }
    
    except Exception as e:
        logger.error('load_products', e)
        raise
    
def load_customers(location_ids, count=5):
    logger = Logger()
    logger.info('load_customers')
    import ast
    if isinstance(location_ids, str):
        location_ids = ast.literal_eval(location_ids)
    try:
        gen = CustomerGenerator()
        conn = Connection(logger).connect()
        loader = CustomerLoader(conn, logger)
        
        customer_data = gen.generate_batch(count, location_ids)
        customer_ids = loader.load_batch(customer_data)
        
        logger.info('load_customers')
        return customer_ids
    
    except Exception as e:
        logger.error('load_customers', e)
        raise

def load_orders(customer_ids, date_ids, product_ids_with_prices, location_ids, count=10):
    logger = Logger()
    logger.info('load_orders')\
    
    # Airflow return ids in a string not in list so I use literal_eval to extract ids from string
    import ast
    if isinstance(customer_ids, str):
        customer_ids = ast.literal_eval(customer_ids)
    
    if isinstance(date_ids, str):
        date_ids = ast.literal_eval(date_ids)

    if isinstance(product_ids_with_prices, str):
        product_ids_with_prices = ast.literal_eval(product_ids_with_prices)

    if isinstance(location_ids, str):
        location_ids = ast.literal_eval(location_ids)
    
    try:
        gen = OrderGenerator()
        conn = Connection(logger).connect() # db
        loader = OrderLoader(conn, logger)
        
        order_data = order_data = gen.generate_batch(
                                    count,
                                    customer_ids,
                                    date_ids,
                                    product_ids_with_prices,
                                    location_ids
                                )
        order_ids = loader.load_batch(order_data)
        
        logger.info('load_orders')
        return order_ids 
    
    except Exception as e:
        logger.error('load_orders', e)
        raise