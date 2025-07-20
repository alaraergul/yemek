from typing import Optional, List

from repository.meal_repository import MealRepository

from model.meal_category import MealCategory
from model.meal_entry import MealEntry

from data_file import categories

class MealService:
  def __init__(self, meal_repository: MealRepository):
    self.meal_repository = meal_repository

  def get_constant_meals(self) -> List[MealCategory]:
    return [MealCategory(**category) for category in categories]

  def get_meal_data(self, user_id: str) -> List[MealEntry]:
    meals = self.meal_repository.get_meals(user_id)

    for meal in meals:
      meal.timestamp *= 1000

    return meals

  def push_meal_data(self, user_id: str, *entries: MealEntry) -> bool:
    return self.meal_repository.push_meal(user_id, *[MealEntry(entry.id, entry.timestamp / 1000, entry.count) for entry in entries])

  def delete_meal_data(self, user_id: str, id: int, timestamp: int) -> bool:
    return self.meal_repository.delete_meal(user_id, id, timestamp)
