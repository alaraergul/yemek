from flask import Blueprint, request

from model.meal_entry import MealEntry

from service.user_service import UserService
from service.meal_service import MealService

meal_blueprint = Blueprint("meal", __name__)
user_service: UserService = None
meal_service: MealService = None

def send_meal_services(_meal_service: MealService, _user_service: UserService):
  global user_service
  global meal_service
  user_service = _user_service
  meal_service = _meal_service

@meal_blueprint.route("/<user_id>", methods = ["GET"])
async def get_user_meals(user_id):
  user = user_service.get_user(user_id)

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    categories = meal_service.get_all_meals()
    return {"success": True, "data": [category.to_dict(user.language) for category in categories]}

@meal_blueprint.route("/<user_id>/data", methods = ["GET"])
async def get_user_meal_data(user_id):
  user = user_service.get_user(user_id)

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    entries = meal_service.get_meal_data(user_id)
    return {"success": True, "data": [entry.to_dict() for entry in entries]}

@meal_blueprint.route("/<user_id>/data", methods = ["POST"])
async def push_user_meal_data(user_id):
  user = user_service.get_user(user_id)

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    success = meal_service.push_meal_data(user.id, *[MealEntry(data["id"], data["timestamp"], data["count"]) for data in request.json])
    return {"success": success}
