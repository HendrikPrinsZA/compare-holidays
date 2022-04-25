import inflect
from loguru import logger
from classes.config import Config
from classes.database import Database

class Model(object):
  
  id: 'id'

  def __init__(self, attributes):
    self.setAttributes(attributes)

  def setAttributes(self, attributes):
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
      logger.warning(f"No record found for {field} = '{value}'")
      return None

    return rows[0]

  @classmethod
  def updateOrCreate(self, attributes:object, values:object=None):
    table = self.table()
    
    conditions = []
    params = {}
    
    for field, value in attributes.items():
      conditions.append(f"{field} = :{field}")
      params[field] = value

    db = Database(Config())
    query = f"SELECT {table}.id FROM {table} WHERE {' AND '.join(conditions)} LIMIT 1;"
    rows = db.execute(query, params)

    if len(rows) == 0:
      logger.warning(f"No record found for '{rows}'")

    return rows[0]