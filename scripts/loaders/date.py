from scripts.loaders.base_loader import BaseLoader

class DateLoader(BaseLoader):
    """Load date dimension data."""
    
    def __init__(self, conn, logger=None):
        super().__init__(conn, logger)
        self.table_name = 'dim_dates'