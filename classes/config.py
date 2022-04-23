from os import environ

class Config:
  db_user = environ.get('DB_USERNAME')
  db_password = environ.get('DB_PASSWORD')
  db_host = environ.get('DB_HOST')
  db_port = environ.get('DB_PORT')
  db_name = environ.get('DB_NAME')