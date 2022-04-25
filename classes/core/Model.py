from datetime import datetime
import sys
import inflect
from loguru import logger
from classes.config import Config
from classes.database import Database

class Model(object):
  def __init__(self, attributes:dict):
    self.setAttributes(attributes)

  def setAttributes(self, attributes:dict):
    self.attributes = attributes

  @classmethod
  def table(self):
    noun = self.__name__

    # Hack: Not sure if inflectEngine is reliable...
    if noun.endswith('ry'):
      return noun.replace('ry', 'ries').lower()

    inflectEngine = inflect.engine()
    return inflectEngine.plural(self.__name__).lower()

  @classmethod
  def firstWhere(self, field, value):
    db = Database(Config())
    table = self.table()

    sql = f"SELECT * FROM {table} WHERE {field} = %({field})s"
    params = {
      f"{field}": value
    }

    rows = db.execute(sql, params)
    
    if len(rows) == 0:
      logger.warning(f"No record found for {table}.{field} = '{value}'")
      return None

    return rows[0]

  @classmethod
  def create(self, fields:dict):
    table = self.table()
    
    # inject audit fields
    fields['created_at'] = datetime.now()
    fields['updated_at'] = fields['created_at']

    strings = []
    for field in fields.keys():
      strings.append(f"{field} = %({field})s")

    queryFields = ", ".join(strings)
    sql = f"INSERT INTO {table} SET {queryFields};"
    db = Database(Config())
    id = db.execute(sql, fields)
    
    return self.firstWhere('id', id)

  @classmethod
  def update(self, fields:dict):
    table = self.table()

    # always expect a field called id
    if not 'id' in fields:
      logger.error(f"Expected field 'id' not found in {fields}")
      sys.exit()
    
    # inject audit fields
    fields['updated_at'] = datetime.now()

    strings = []
    for field in fields.keys():
      if field == 'id':
        continue

      strings.append(f"{field} = %({field})s")

    queryFields = ", ".join(strings)
    sql = f"UPDATE {table} SET {queryFields} WHERE id = %(id)s;"
    db = Database(Config())
    db.execute(sql, fields)

    return self.firstWhere('id', fields['id'])

  @classmethod
  def updateOrCreate(self, fieldsToMatch:dict, fieldsToUpdate:object=None):
    table = self.table()
    
    strings = []
    for field in fieldsToMatch.keys():
      strings.append(f"{field} = %({field})s")

    db = Database(Config())
    sql = f"SELECT {table}.id FROM {table} WHERE {' AND '.join(strings)} LIMIT 1;"
    rows = db.execute(sql, fieldsToMatch)

    if len(rows) > 1:
      logger.error(f"Found many rows, but expected only 1. SQL: {sql}")
      sys.exit()

    if len(rows) == 0:
      record = self.create(fieldsToMatch)
      id = record['id']
    else:
      id = rows[0]['id']

    if fieldsToUpdate is not None:
      fieldsToUpdate['id'] = id
      self.update(fieldsToUpdate)

    return self.firstWhere('id', id)