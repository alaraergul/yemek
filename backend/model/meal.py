from typing import List

from model.user import Language

class Meal:
  def __init__(self, id: int, names: List[str], quantity: int, purine: float, kcal: float, sugar: float):
    self.id = id
    self.names = names # ["turkish name", "english name"]
    self.quantity = quantity
    self.purine = purine
    self.kcal = kcal
    self.sugar = sugar

  def to_dict(self, language: Language):
    return {
      "id": self.id,
      "name": self.names[language],
      "quantity": self.quantity,
      "purine": self.purine,
      "kcal": self.kcal,
      "sugar": self.sugar
    }
