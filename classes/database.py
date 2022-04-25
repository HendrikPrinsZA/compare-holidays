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
    finally:
      logger.info('Connection opened successfully.')

  def getValueTypeSymbol(self, value:any):
    valueTypeSymbols = {
      bool: '%b',
      int: '%d',
      float: '%f',
      str: '%s'
    }

    valueType = type(value)
    if not valueType in valueTypeSymbols:
      logger.error(f"Unsupported value type of {valueType} for '%s'".format(value))
      sys.exit(1)

    return valueTypeSymbols[valueType]

  def sqlInjectParams(self, sql:str, params:object):
    keys = list(params)
    if len(keys) == 0:
      return sql

    key = keys[0]
    value = params[key]
    sql = self.sqlInjectParam(sql, key, value)
    del params[key]

    return self.sqlInjectParams(sql, params)

  def sqlInjectParam(self, sql:str, key:str, value:str):
    # format natively in Python 
    # - https://stackoverflow.com/a/5785163/7403334
    # - https://pymysql.readthedocs.io/en/latest/modules/cursors.html#pymysql.cursors.Cursor.execute
    valueTypeSymbol = self.getValueTypeSymbol(value)
    
    find = f":{key}"
    replace = f"%{key}"

    if not find in sql:
      logger.error(f"Could not find argument {find} in {sql}")
      sys.exit(1)

    return sql.replace(f":{key}", f"{replace}")
    
  def replaceSqlParamsWithSymbols(self, sql:str, params:dict):
    keys = list(params.keys())
    if len(keys) == 0:
      return sql

    key = keys[0]
    value = params[key]
    sql = self.sqlInjectParam(sql, key, value)
    del params[key]

    return self.replaceSqlParamsWithSymbols(sql, params)

  def splitSqlAndParams(self, sql:str, params:dict):
    values = [*params.values()]
    sql = self.replaceSqlParamsWithSymbols(sql, params)
    return {
      'sql': sql,
      'params': values
    }

  def execute(self, sql:str, params:dict):
    # parts = self.splitSqlAndParams(sql, params)
    # sql = parts['sql']
    params = params

    logger.info(f"Executing\n{sql}\n{params}")

    # open the mysql connection
    try:
      self.open_connection()

      # write to cursor
      with self.conn.cursor() as cursor:
        rowsAffected = cursor.execute(sql, params)

        # select logic returns rows
        if sql.lower().startswith('select'):
          rows = cursor.fetchall()
          cursor.close()
          return rows

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

    print(parts)
    sys.exit(1)

    sql = self.sqlInjectParams(sql, params)

    # paramValues = 

    try:
      self.open_connection()
      with self.conn.cursor() as cur:

        # Select logic
        if sql.lower().startswith('select'):
          records = []
          print(f"Executing {sql}")
          sys.exit()
          cur.execute(sql)
          result = cur.fetchall()
          for row in result:
            records.append(row)
          cur.close()
          return records
        
        # All other execs (assuming rows effected)
        result = cur.execute(sql)
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