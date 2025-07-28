from flask import Blueprint, request

from service.user_service import UserService
from service.water_consumption_service import WaterConsumptionService

water_consumption_blueprint = Blueprint("water_consumption", __name__)
user_service: UserService = None
water_consumption_service: WaterConsumptionService = None

def send_water_consumption_services(_water_consumption_service: WaterConsumptionService, _user_service: UserService):
  global user_service
  global water_consumption_service
  user_service = _user_service
  water_consumption_service = _water_consumption_service

@water_consumption_blueprint.route("/<user_id>", methods = ["GET"])
def get_user_water_consumption(user_id):
  user = user_service.get_user(user_id)

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    entries = water_consumption_service.get_water_consumption(user_id)
    return {"success": True, "data": [entry.to_dict() for entry in entries]}

@water_consumption_blueprint.route("/<user_id>", methods = ["POST"])
def push_user_water_consumption(user_id):
  user = user_service.get_user(user_id)

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    success = water_consumption_service.push_water_consumption(user.id, request.json["value"], request.json["timestamp"])
    return {"success": success}
