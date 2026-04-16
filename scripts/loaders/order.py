from scripts.loaders.base_loader import BaseLoader

class OrderLoader(BaseLoader):
    """Load orders (fact table) data."""
    
    def __init__(self, conn, logger=None):
        super().__init__(conn, logger)
        self.table_name = 'fact_orders'