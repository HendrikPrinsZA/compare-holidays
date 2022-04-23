class Database:
  def __init__(self, config):
    self.host = config.db_host
    self.username = config.db_user
    self.password = config.db_password
    self.port = config.db_port
    self.dbname = config.db_name
    self.conn = None