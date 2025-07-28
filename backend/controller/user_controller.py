from flask import Blueprint, request
from service.user_service import UserService

user_blueprint = Blueprint("user", __name__)
user_service: UserService = None

def send_user_services(service: UserService):
  global user_service
  user_service = service

@user_blueprint.route("/", methods = ["GET"])
def get_users():
  return user_service.get_all_users()

@user_blueprint.route("/<user_id>", methods = ["GET"])
def get_user(user_id):
  user = user_service.get_user(user_id)

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    return {"success": True, "data": user.to_dict()}

@user_blueprint.route("/<user_id>", methods = ["PATCH"])
def edit_user(user_id):
  success = user_service.edit_user(user_id, request.json["username"], request.json["password"],
    request.json["gender"], request.json["language"], request.json["weight"], request.json["firstName"],
    request.json["lastName"], request.json["purineLimit"], request.json["kcalLimit"], request.json["sugarLimit"]
  )

  return {"success": success}

@user_blueprint.route("/login", methods = ["POST"])
def login_user():
  user = user_service.login_user(request.json["username"], request.json["password"])

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    return {"success": True, "data": user.to_dict()}

@user_blueprint.route("/register", methods = ["POST"])
def register_user():
  user = user_service.register_user(request.json["username"], request.json["password"], request.json["gender"], request.json["language"], request.json["weight"], request.json["firstName"], request.json["lastName"])

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    return {"success": True, "data": user.to_dict()}
