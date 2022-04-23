import sys
import pymysql
from loguru import logger

from classes.config import Config

class Database:
  def __init__(self, config:Config):
    self.host = config.db_host
    self.user = config.db_user
    self.password = config.db_password
    self.port = int(config.db_port)
    self.db = config.db_name
    self.conn = None

  def open_connection(self):
    try:
      if self.conn is None:
        self.conn = pymysql.connect(
          host=self.host,
          user=self.user,
          password=self.password,
          database=self.db,
          port=self.port,
          cursorclass=pymysql.cursors.DictCursor,
          connect_timeout=5
        )
    except pymysql.MySQLError as e:
      logger.error(e)
      sys.exit()
    finally:
      logger.info('Connection opened successfully.')

  def run_query(self, query):
    try:
      self.open_connection()
      with self.conn.cursor() as cur:
        if 'SELECT' in query:
          records = []
          cur.execute(query)
          result = cur.fetchall()
          for row in result:
            records.append(row)
          cur.close()
          return records
        
        result = cur.execute(query)
        self.conn.commit()
        affected = f"{cur.rowcount} rows affected."
        cur.close()
        return affected
    except pymysql.MySQLError as e:
      logger.error(e)
      sys.exit()
    finally:
      if self.conn:
        self.conn.close()
        self.conn = None
        logger.info('Database connection closed.')