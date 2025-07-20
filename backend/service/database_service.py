import psycopg2
from os import getenv

class DatabaseService:
  def __init__(self):
    self.conn = psycopg2.connect(
      database = getenv("DATABASE_NAME"),
      user = getenv("DATABASE_USER"),
      password = getenv("DATABASE_PASS"),
      host = getenv("DATABASE_HOST")
    )

  def get_cursor(self):
    return self.conn.cursor()

  def commit(self):
    self.conn.commit()
