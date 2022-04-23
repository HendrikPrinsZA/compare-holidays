from os import environ, path
import sys
from dotenv import load_dotenv
from loguru import logger

pathEnv = path.abspath(f"{path.dirname(__file__)}/../.env")

if not path.isfile(pathEnv):
  logger.error(f"Config file not found: {pathEnv}")
  sys.exit()

load_dotenv(pathEnv)

class Config:
  def __init__(self):
    self.db_user = environ.get('DB_USERNAME')
    self.db_password = environ.get('DB_PASSWORD')
    self.db_host = environ.get('DB_HOST')
    self.db_port = environ.get('DB_PORT_FORWARD')
    self.db_name = environ.get('DB_DATABASE')