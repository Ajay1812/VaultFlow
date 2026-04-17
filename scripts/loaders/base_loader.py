from scripts.core.connection import Connection
from scripts.core.logger import Logger

class BaseLoader:
    def __init__(self, conn, logger=None):
        self.logger = logger or Logger()
        self.conn = conn or Connection(self.logger)
        self.table_name = None
    
    def load(self, data):
        if not self.table_name:
            raise NotImplementedError("Subclass must define table_name")
        
        # Dynamically build INSERT SQL
        columns = ', '.join(data.keys())  # 'city, state, region, pincode'
        placeholders = ', '.join(['%s'] * len(data))  # '%s, %s, %s, %s'
        values = list(data.values())  # ['Delhi', 'Delhi', 'North', '110001']
        
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)  
            returned_id = cur.fetchone()[0] 
            self.conn.commit()
            self.logger.success(self.table_name, 1)
            return returned_id
        except Exception as e:
            self.conn.rollback()  
            self.logger.error(self.table_name, e)
            raise
    def load_batch(self, data_list):
        ids = []
        for data in data_list:
            ids.append(self.load(data))
        self.logger.success(self.table_name, len(ids))  # One log entry for batch
        return ids