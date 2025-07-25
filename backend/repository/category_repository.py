from typing import List

from service.database_service import DatabaseService

from model.meal import Meal
from model.meal_category import MealCategory

class CategoryRepository:
  def __init__(self, db: DatabaseService):
    self.db = db

    self.db.get_cursor().execute("CREATE TABLE IF NOT EXISTS categories(" \
      "id int PRIMARY KEY,"
      "names text[2] NOT NULL"
    ");")

    self.db.commit()

  def get_categories(self) -> List[MealCategory]:
    cur = self.db.get_cursor()
    cur.execute("SELECT * FROM categories;")
    categories = cur.fetchall()

    return [MealCategory(category[0], category[1], []) for category in categories]
