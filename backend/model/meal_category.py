from typing import List

from model.user import Language
from model.meal import Meal

class MealCategory:
  def __init__(self, names: List[str], meals: List[Meal]):
    self.names = names # ["turkish name", "english name"]
    self.meals: List[Meal] = []

    for meal in meals:
      self.meals.append(meal)

  def to_dict(self, language: Language):
    return {
      "name": self.names[language],
      "meals": [meal.to_dict(language) for meal in self.meals]
    }
