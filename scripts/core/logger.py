import logging

class Logger:
    def __init__(self):
        try:
            from airflow.utils.log.logging_mixin import LoggingMixin
            self.logger = LoggingMixin().log
        except Exception:
            logging.basicConfig(
                format="%(asctime)s %(levelname)s: %(message)s",
                level=logging.INFO,
            )
            self.logger = logging.getLogger(__name__)

    def info(self, message: str):
        self.logger.info(message)

    def success(self, table: str, rows: int):
        self.logger.info(f"{table} → {rows} rows inserted")

    def error(self, context: str, error: Exception):
        self.logger.error(f"{context} → {error}")