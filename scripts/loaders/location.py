from scripts.loaders.base_loader import BaseLoader

class LocationLoader(BaseLoader):
    
    def __init__(self, conn, logger=None):
        super().__init__(conn, logger)
        self.table_name = 'dim_locations'
        