from flask import Blueprint, Response, request, stream_with_context
from gevent.queue import Queue

from service.user_service import UserService
from service.meal_service import MealService

custom_meal_blueprint = Blueprint("custom_meal", __name__)
user_service: UserService = None
meal_service: MealService = None

def send_custom_meal_services(_meal_service: MealService, _user_service: UserService):
  global meal_service
  global user_service
  meal_service = _meal_service
  user_service = _user_service

@custom_meal_blueprint.route("/", methods = ["GET"])
def get_custom_meals():
  user = user_service.login_user(request.json["username"], request.json["password"])

  if user is None:
    return {"success": False, "message": "Unauthorized access."}, 403
  else:
    meals = meal_service.get_custom_meals()
    return {"success": True, "data": [meal.to_dict(user.language) for meal in meals]}

@custom_meal_blueprint.route("/", methods = ["POST"])
def post_custom_meal():
  user = user_service.login_user(request.json["username"], request.json["password"])

  if user is None:
    return {"success": False, "message": "Unauthorized access."}, 403
  else:
    meal = meal_service.push_custom_meal(request.json["names"], request.json["quantity"], request.json["purine"], request.json["sugar"], request.json["kcal"])

    if meal is None:
      return {"success": False, "message": "Custom meal cannot be pushed."}
    else:
      return {"success": True, "data": meal.to_dict(user.language)}

@custom_meal_blueprint.route("/events")
def stream_custom_meals(): # async is blocked because of sse
  queue = Queue()
  meal_service.subscriptions.append(queue)
  return Response(stream_with_context(meal_service.stream_custom_meals(queue)), mimetype="text/event-stream")
