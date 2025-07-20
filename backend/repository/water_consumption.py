from typing import List

from service.database_service import DatabaseService

from model.water_consumption import WaterConsumption, WaterValue

class WaterConsumptionRepository:
  def __init__(self, db: DatabaseService):
    self.db = db

    self.db.get_cursor().execute("CREATE TABLE IF NOT EXISTS water_consumption(" \
      "user_id uuid references users(id)," \
      "value bit NOT NULL," \
      "timestamp timestamp NOT NULL"
    ");")

    self.db.commit()

  def get_water_consumption(self, user_id: str) -> List[WaterConsumption]:
    cur = self.db.get_cursor()
    cur.execute("SELECT value, extract(epoch from timestamp) FROM water_consumption WHERE user_id=%s;", (user_id,))
    entries = cur.fetchall()

    return [WaterConsumption(entry[0], entry[1]) for entry in entries]

  def push_water_consumption(self, user_id: str, value: WaterValue, timestamp: int) -> bool:
    cur = self.db.get_cursor()
    cur.execute("INSERT INTO water_consumption (user_id, value, timestamp) VALUES (%s, B'%s', to_timestamp(%s))", (user_id, value, timestamp))
    self.db.commit()

    return cur.rowcount == 1
