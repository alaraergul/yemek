from enum import IntEnum

class Gender(IntEnum):
  MALE = 0
  FEMALE = 1

class Language(IntEnum):
  TURKISH = 0
  ENGLISH = 1

class User:
  def __init__(
    self, id: str, username: str, password: str, weight: int, gender: Gender, language: Language,
    purine_limit: int, sugar_limit: int, kcal_limit: int, first_name: str, last_name: str
  ):
    self.id = id
    self.username = username
    self.password = password
    self.weight = weight
    self.gender = int(gender)
    self.language = int(language)
    self.purine_limit = purine_limit
    self.sugar_limit = sugar_limit
    self.kcal_limit = kcal_limit
    self.first_name = first_name
    self.last_name = last_name

  def to_dict(self):
    return {
      "id": self.id,
      "weight": self.weight,
      "gender": self.gender,
      "language": self.language,
      "purineLimit": self.purine_limit,
      "sugarLimit": self.sugar_limit,
      "kcalLimit": self.kcal_limit,
      "firstName": self.first_name,
      "lastName": self.last_name
    }
