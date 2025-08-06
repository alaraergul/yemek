from typing import Optional, List

from repository.user_repository import UserRepository
from model.user import User, Language, Gender

from service.meal_service import MealService
from service.water_consumption_service import WaterConsumptionService

class UserService:
  def __init__(self, user_repository: UserRepository):
    self.user_repository = user_repository

  def set_services(self, meal_service: MealService, water_consumption_service: WaterConsumptionService):
    self.meal_service = meal_service
    self.water_consumption_service = water_consumption_service

  def delete_user_account(self, user_id: str) -> bool:
    self.meal_service.delete_user_all_meals(user_id)
    self.water_consumption_service.delete_user_all_consumption(user_id)
    return self.user_repository.delete_user(user_id)

  def get_all_users(self) -> List[User]:
    return self.user_repository.get_all_users()

  def get_user(self, id: str) -> Optional[User]:
    return self.user_repository.get_user(id)

  def login_user(self, username: str, password: str) -> Optional[User]:
    return self.user_repository.login(username, password)

  def register_user(self, username: str, password: str, gender: Gender, language: Language, weight: int, first_name: str, last_name: str) -> Optional[User]:
    if self.user_repository.exists_user(username):
      return None
    else:
      id = self.user_repository.register(username, password, language, gender, weight, first_name, last_name)
      return self.user_repository.get_user(id)

  def edit_user(self, user_id: str, username: str, password: str,
    gender: Gender, language: Language, weight: int, first_name: str, last_name: str,
    purine_limit: Optional[int], kcal_limit: Optional[int], sugar_limit: Optional[int]
  ) -> bool:
    id = self.user_repository.get_user_id(username, password)

    if id == user_id:
      return self.user_repository.edit_user(id, gender, language, weight, first_name, last_name, purine_limit, kcal_limit, sugar_limit)
    else:
      return False