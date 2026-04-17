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
    logger.info('Starting load_locations')
    conn = None
    try:
        gen = LocationGenerator()
        conn = Connection(logger).connect() # db
        loader = LocationLoader(conn, logger)
        
        location_data = gen.generate_batch(count)
        location_ids = loader.load_batch(location_data)
        
        logger.info('Completed load_locations')
        return location_ids  # XCom: passed to downstream tasks
    
    except Exception as e:
        logger.error(f'load_locations failed {e}')
        raise
    finally:
        if conn:
            conn.close()
    
def load_dates(count=5):
    logger = Logger()
    logger.info('Starting load_dates')
    conn = None
    try:
        gen = DateGenerator()
        conn = Connection(logger).connect() # db
        loader = DateLoader(conn, logger)
        
        date_data = gen.generate_batch(count)
        date_ids = loader.load_batch(date_data)
        
        logger.info('Completed load_dates')
        return date_ids  
    
    except Exception as e:
        logger.error(f'load_dates failed: {e}')
        raise
    finally:
        if conn:
            conn.close()
    
    
def load_products(count=5):
    logger = Logger()
    logger.info('Starting load_products')
    conn = None
    try:
        gen = ProductGenerator()
        conn = Connection(logger).connect() # db
        loader = ProductLoader(conn, logger)
        
        product_data = gen.generate_batch(count)
        product_ids = loader.load_batch(product_data)
        
        logger.info('Completed load_products')
        return {
            pid: product_data[i]['unit_price']
            for i, pid in enumerate(product_ids)
        }
    
    except Exception as e:
        logger.error(f'load_products failed: {e}')
        raise
    finally:
        if conn:
            conn.close()
    
    
def load_customers(count=5, **context):
    logger = Logger()
    logger.info('Starting load_customers')
    conn = None
    ti = context['task_instance'] # get data from XCom 
    location_ids = ti.xcom_pull(task_ids='generating_location_ids')
    if not location_ids:
        raise ValueError('No location_ids received from XCom')
    
    try:
        gen = CustomerGenerator()
        conn = Connection(logger).connect()
        loader = CustomerLoader(conn, logger)
        
        customer_data = gen.generate_batch(count, location_ids)
        customer_ids = loader.load_batch(customer_data)
        
        logger.info('Completed load_customers')
        return customer_ids
    
    except Exception as e:
        logger.error(f'load_customers failed: {e}')
        raise
    finally:
        if conn:
            conn.close()
    

def load_orders(count=10, **context):
    logger = Logger()
    logger.info('Starting load_orders')
    conn = None
    try:
        ti = context['task_instance'] # get data from XCom 
        customer_ids = ti.xcom_pull(task_ids='generating_customer_ids')
        date_ids = ti.xcom_pull(task_ids='generating_date_ids')
        product_ids_with_prices = ti.xcom_pull(task_ids='generating_product_ids')
        location_ids = ti.xcom_pull(task_ids='generating_location_ids')
        
        if not customer_ids:
            raise ValueError('No customer_ids received from XCom')
        if not date_ids:
            raise ValueError('No date_ids received from XCom')
        if not product_ids_with_prices:
            raise ValueError('No product_ids received from XCom')
        if not location_ids:
            raise ValueError('No location_ids received from XCom')
        
        gen = OrderGenerator()
        conn = Connection(logger).connect()
        loader = OrderLoader(conn, logger)
        
        order_data = gen.generate_batch(
            count,
            customer_ids,
            date_ids,
            product_ids_with_prices,
            location_ids
        )
        order_ids = loader.load_batch(order_data)
        
        logger.info('Completed load_orders')
        return order_ids
    
    except Exception as e:
        logger.error(f'load_orders failed: {e}')
        raise
    finally:
        if conn:
            conn.close()
        