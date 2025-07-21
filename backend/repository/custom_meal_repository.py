from typing import List, Optional

from service.database_service import DatabaseService

from model.meal import Meal

class CustomMealRepository:
  def __init__(self, db: DatabaseService):
    self.db = db

    self.db.get_cursor().execute("""
      CREATE TABLE IF NOT EXISTS custom_meals (
        id serial PRIMARY KEY,
        names text[2] NOT NULL,
        quantity int NOT NULL,
        purine float NOT NULL,
        sugar float NOT NULL,
        kcal float NOT NULL
      );

      DO $$
      BEGIN
        IF EXISTS (
          SELECT 1 FROM pg_class WHERE relkind = 'S' AND relname = 'custom_meals_id_seq'
        ) THEN
          ALTER SEQUENCE custom_meals_id_seq RESTART WITH 300;
        END IF;
      END
      $$;
    """)
    self.db.commit()

  def get_custom_meals(self) -> List[Meal]:
    cur = self.db.get_cursor()
    cur.execute("SELECT id, names, quantity, purine, kcal, sugar FROM custom_meals;")
    meals = cur.fetchall()

    return [Meal(meal[0], meal[1], meal[2], meal[3], meal[4], meal[5]) for meal in meals]

  def push_custom_meal(self, names: List[str], quantity: int, purine: float, sugar: float, kcal: float) -> Optional[Meal]:
    cur = self.db.get_cursor()
    cur.execute("INSERT INTO custom_meals (names, quantity, purine, sugar, kcal) VALUES (%s, %s, %s, %s, %s) RETURNING id;", (
      names, quantity, purine, sugar, kcal
    ))

    self.db.commit()
    id = cur.fetchone()[0]

    return Meal(id, names, quantity, purine, kcal, sugar)
