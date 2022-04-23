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

    if noun.endswith('ry'):
      return noun.replace('ry', 'ries').lower()

    inflectEngine = inflect.engine()
    return inflectEngine.plural(self.__name__).lower()

  @classmethod
  def firstWhere(self, field, value):
    table = self.table()

    db = Database(Config())
    query = f"SELECT * FROM {table} WHERE {field} = '{value}' LIMIT 1;"
    rows = db.run_query(query)

    if len(rows) == 0:
      logger.warning(f"No record found for {field} = '{value}'")

    return rows[0]

  @classmethod
  def updateOrCreate(self, attributes:object, values:object=None):
    table = self.table()

    conditions = []

    for field, value in attributes.__dict__.items():
      conditions.append(f"{field} = '{value}'")

    db = Database(Config())
    query = f"SELECT {self.id} FROM {table} WHERE {' AND '.join(conditions)}' LIMIT 1;"
    rows = db.run_query(query)

    if len(rows) == 0:
      logger.warning(f"No record found for ")

    return rows[0]