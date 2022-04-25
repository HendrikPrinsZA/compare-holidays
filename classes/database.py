from concurrent.futures import process
import pprint
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

  def execute(self, sql:str, params:dict):
    try:
      self.open_connection()
      with self.conn.cursor() as cursor:
        rowsAffected = cursor.execute(sql, params)

        # select logic returns rows
        if sql.lower().startswith('select'):
          rows = cursor.fetchall()
          cursor.close()
          return rows

        # insert into returns last insert id
        if sql.lower().startswith('insert into'):
          self.conn.commit()
          id = cursor.lastrowid
          cursor.close()
          return id

        # all other logic returns rows effected
        self.conn.commit()
        affected = f"{rowsAffected} rows affected."
        cursor.close()
        return affected
    
    except pymysql.MySQLError as e:
      logger.error(e)
      sys.exit()

    finally:
      if self.conn:
        self.conn.close()
        self.conn = None