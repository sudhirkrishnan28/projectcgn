import pymysql
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DB_manager:
    @staticmethod
    def get_db_connection():
        try:
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                passwd='sudhir2807',
                db='phone',
                connect_timeout=5
            )
            logger.info("Successfully connected to the database.")
            return connection
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            raise
