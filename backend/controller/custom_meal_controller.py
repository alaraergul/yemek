from flask import Blueprint, request
from typing import Optional
import json

from model.meal import Meal

from service.user_service import UserService
from service.meal_service import MealService
from service.sse_service import SseService

custom_meal_blueprint = Blueprint("custom_meal", __name__)
user_service: UserService = None
meal_service: MealService = None
sse_service: SseService = None

def send_custom_meal_services(_sse_service: SseService, _meal_service: MealService, _user_service: UserService):
  global meal_service
  global user_service
  global sse_service
  meal_service = _meal_service
  user_service = _user_service
  sse_service = _sse_service

@custom_meal_blueprint.route("/", methods = ["GET"])
async def get_custom_meals():
  user = user_service.login_user(request.json["username"], request.json["password"])

  if user is None:
    return {"success": False, "message": "Unauthorized access."}, 403
  else:
    meals = meal_service.get_custom_meals()
    return {"success": True, "data": [meal.to_dict(user.language) for meal in meals]}

@custom_meal_blueprint.route("/", methods = ["POST"])
async def post_custom_meal():
  user = user_service.login_user(request.json["username"], request.json["password"])

  if user is None:
    return {"success": False, "message": "Unauthorized access."}, 403
  else:
    meal = meal_service.push_custom_meal(request.json["names"], request.json["quantity"], request.json["purine"], request.json["sugar"], request.json["purine"])

    if meal is None:
      return {"success": False, "message": "Custom meal cannot be pushed."}
    else:
      sse_service.sse_send_to_all(json.dumps(meal))
      return {"success": True, "data": meal.to_dict(user.language)}
