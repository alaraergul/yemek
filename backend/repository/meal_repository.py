from typing import List

from service.database_service import DatabaseService

from model.meal import Meal
from model.meal_entry import MealEntry

class MealRepository:
  def __init__(self, db: DatabaseService):
    self.db = db

    self.db.get_cursor().execute("CREATE TABLE IF NOT EXISTS meals(" \
      "userid uuid references users(id)," \
      "id int NOT NULL," \
      "timestamp timestamp NOT NULL," \
      "count float NOT NULL"
    ");")

    self.db.commit()

  def get_meals(self, user_id: str) -> List[MealEntry]:
    cur = self.db.get_cursor()
    cur.execute("SELECT id, extract(epoch from timestamp), count FROM meals WHERE userid=%s;", (user_id,))
    entries = cur.fetchall()

    return [MealEntry(entry[0], float(entry[1]), entry[2]) for entry in entries]

  def push_meal(self, user_id: str, *entries: MealEntry) -> bool:
    cur = self.db.get_cursor()
    args = b",".join(cur.mogrify("(%s, %s, to_timestamp(%s), %s)", (user_id, entry.id, entry.timestamp, entry.count)) for entry in entries).decode("utf-8")
    cur.execute(f"INSERT INTO meals (userid, id, timestamp, count) VALUES {args}")
    self.db.commit()

    return cur.rowcount == len(entries)

  def delete_meal(self, user_id: str, id: int, timestamp: float) -> bool:
    cur = self.db.get_cursor()
    cur.execute("DELETE FROM meals WHERE userid=%s AND id=%s AND timestamp=to_timestamp(%s);", (user_id, id, timestamp))
    self.db.commit()

    return cur.rowcount == 1
  
  def delete_user_meals(self, user_id: str) -> bool:
    cur = self.db.get_cursor()
    cur.execute("DELETE FROM meals WHERE userid=%s;", (user_id,))
    self.db.commit()
    return cur.rowcount >= 0