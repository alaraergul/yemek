from typing import List

from service.database_service import DatabaseService

from model.meal import Meal
from model.meal_category import MealCategory

class ConstantMealRepository:
  def __init__(self, db: DatabaseService):
    self.db = db

    self.db.get_cursor().execute("CREATE TABLE IF NOT EXISTS constant_meals(" \
      "id int PRIMARY KEY,"
      "category_id int references categories(id),"
      "names text[2] NOT NULL,"
      "purine float NOT NULL,"
      "kcal float NOT NULL,"
      "sugar float NOT NULL,"
      "quantity float NOT NULL"
    ");")

    self.db.commit()

  def get_constant_meals_of_category(self, category_id: int):
    cur = self.db.get_cursor()
    cur.execute("SELECT id, names, quantity, purine, kcal, sugar FROM constant_meals WHERE category_id = %s;", (category_id,))

    return cur.fetchall()
