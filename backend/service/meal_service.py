from typing import List, Optional
from json import dumps
from gevent.queue import Queue

from repository.meal_repository import MealRepository
from repository.category_repository import CategoryRepository
from repository.constant_meal_repository import ConstantMealRepository
from repository.custom_meal_repository import CustomMealRepository

from model.meal_category import MealCategory
from model.meal_entry import MealEntry
from model.meal import Meal

class MealService:
  def __init__(self,
      meal_repository: MealRepository, custom_meal_repository: CustomMealRepository,
      category_repository: CategoryRepository, constant_meal_repository: ConstantMealRepository
  ):
    self.meal_repository = meal_repository
    self.custom_meal_repository = custom_meal_repository
    self.category_repository = category_repository
    self.constant_meal_repository = constant_meal_repository
    self.subscriptions: List[Queue] = []

  def get_constant_meals(self) -> List[MealCategory]:
    categories = self.category_repository.get_categories()

    for category in categories:
      category.meals = [Meal(*meal) for meal in self.constant_meal_repository.get_constant_meals_of_category(category.id)]

    return categories

  def get_custom_meals(self) -> List[Meal]:
    return self.custom_meal_repository.get_custom_meals()

  def get_all_meals(self) -> List[MealCategory]:
    customCategory = MealCategory(-1, ["Özel Yemekler", "Custom Meals"], self.custom_meal_repository.get_custom_meals())
    return [customCategory] + self.get_constant_meals()

  def push_custom_meal(self, names: List[str], quantity: int, purine: float, sugar: float, kcal: float) -> Optional[Meal]:
    response = self.custom_meal_repository.push_custom_meal(names, quantity, purine, sugar, kcal)

    if response == False:
      return response

    for queue in self.subscriptions:
      queue.put(dumps({"id": response.id, "names": names, "quantity": quantity, "purine": purine, "sugar": sugar, "kcal": kcal}))

    return response

  def stream_custom_meals(self, queue: Queue):
    try:
      while True:
        data = queue.get()
        yield f"data: {data}\n\n"
    except GeneratorExit:
      self.subscriptions.remove(queue)

  def get_meal_data(self, user_id: str) -> List[MealEntry]:
    meals = self.meal_repository.get_meals(user_id)

    for meal in meals:
      meal.timestamp *= 1000

    return meals

  def push_meal_data(self, user_id: str, *entries: MealEntry) -> bool:
    return self.meal_repository.push_meal(user_id, *[MealEntry(entry.id, entry.timestamp / 1000, entry.count) for entry in entries])

  def delete_meal_data(self, user_id: str, id: int, timestamp: int) -> bool:
    return self.meal_repository.delete_meal(user_id, id, timestamp / 1000)
  
  def delete_user_all_meals(self, user_id: str) -> bool:
    return self.meal_repository.delete_user_meals(user_id)