import psycopg2
from sqlalchemy import create_engine
from scripts.core.config import Config
from scripts.core.logger import Logger

class Connection:
    def __init__(self, logger):
        self.logger = logger or Logger()
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=Config.HOST,
                port=Config.PORT,
                database=Config.DATABASE,
                user=Config.USER,
                password=Config.PASSWORD
            )
            self.logger.info(f'Connected to DB: {Config.DATABASE}')
            return self.conn
        except psycopg2.OperationalError as e:
            self.logger.error('Connection Error:', e)
            raise Exception("Database connection failed")

    def get_engine(self):
        # SQLAlchemy engine for pandas read_sql
        url = (
            f"postgresql+psycopg2://"
            f"{Config.USER}:{Config.PASSWORD}"
            f"@{Config.HOST}:{Config.PORT}"
            f"/{Config.DATABASE}"
        )
        return create_engine(url)
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.logger.info('Connection closed')