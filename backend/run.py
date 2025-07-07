from flask import Flask, request, Request, render_template
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, db
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("./firebase-key.json")
firebase = initialize_app(cred, {
  "databaseURL": getenv("FIREBASE_URL")
})

@app.route("/")
def home():
    return render_template('index.html')

def check_is_valid_json(req: Request, element_count: int):
  if not req.is_json or not isinstance(req.json, dict):
    return {"code": 400, "message": "Body must be a JSON object."}

  if len(req.json) != element_count:
    return {"code": 400, "message": f"Body must contain exactly {element_count} members."}

  return ""

@app.route("/users/<user_id>", methods = ["POST"])
def post_meal(user_id):
  ref = db.reference(f"/{user_id}")

  if (error := check_is_valid_json(request, 3)) != "":
    return error

  if not "id" in request.json or not isinstance(request.json["id"], int):
    return {"code": 400, "message": "Body must contain \"id\" key and it must be a number."}

  if not "count" in request.json or not isinstance(request.json["count"], int):
    return {"code": 400, "message": "Body must contain \"count\" key and it must be a number."}

  if not "timestamp" in request.json or not isinstance(request.json["timestamp"], int):
    return {"code": 400, "message": "Body must contain \"timestamp\" key and it must be a number that represents unix timestamp."}

  ref.push(request.json)
  return ""

@app.route("/users/<user_id>", methods = ["GET"])
def get_meal(user_id):
  ref = db.reference(f"/{user_id}")
  data: dict = ref.get()

  if data == None:
    return list()
  else:
    return list(data.values())

@app.route("/users/<user_id>", methods = ["DELETE"])
def delete_meal(user_id):
  if (error := check_is_valid_json(request, 2)) != "":
    return error

  if not "id" in request.json or not isinstance(request.json["id"], int):
    return {"code": 400, "message": "Body must contain \"id\" key and it must be a number."}

  if not "timestamp" in request.json or not isinstance(request.json["timestamp"], int):
    return {"code": 400, "message": "Body must contain \"timestamp\" key and it must be a number that represents unix timestamp."}

  ref = db.reference(f"/{user_id}")
  data: dict = ref.get()
  new_data = dict()

  for key, value in data.items():
    if value["id"] != request.json["id"] or value["timestamp"] != request.json["timestamp"]:
      new_data[key] = value

  ref.set(new_data)
  return ""

@app.route("/users", methods = ["GET"])
def get_users():
  ref = db.reference("/users")
  data: dict = ref.get()

  if data == None:
    return list()
  else:
    return list(data.keys())

@app.route("/users/register", methods = ["POST"])
def create_new_user():
  if (error := check_is_valid_json(request, 3)) != "":
    return error

  if not "username" in request.json or not isinstance(request.json["username"], str):
    return {"code": 400, "message": "Body must contain \"username\" key and it must be a string."}

  if not "password" in request.json or not isinstance(request.json["password"], str):
    return {"code": 400, "message": "Body must contain \"password\" key and it must be a string."}

  if not "weight" in request.json or not isinstance(request.json["weight"], int):
    return {"code": 400, "message": "Body must contain \"weight\" key and it must be a string."}

  ref = db.reference("/users")
  ref_dict: dict = ref.get();

  for key, value in ref_dict.items():
    if value["username"] == request.json["username"]:
      return {"code": 403, "message": "This user already exists."}

  ref = ref.push(request.json)

  return {"id": ref.key, "weight": request.json["weight"]}

@app.route("/users/login", methods = ["POST"])
def check_user_credientals():
  if (error := check_is_valid_json(request, 2)) != "":
    return error

  if not "username" in request.json or not isinstance(request.json["username"], str):
    return {"code": 400, "message": "Body must contain \"username\" key and it must be a string."}

  if not "password" in request.json or not isinstance(request.json["password"], str):
    return {"code": 400, "message": "Body must contain \"password\" key and it must be a string."}

  ref = db.reference("/users")

  if ref == None:
    return {"code": 404, "message": "There is no user"}

  users: dict = ref.get()

  for key, value in users.items():
    if value["username"] == request.json["username"] and value["password"] == request.json["password"]:
      return {"id": key, "weight": value["weight"]}

  return {"code": 403, "message": "Wrong credientals"}

if __name__ == "__main__":
  app.run(port = 8087, host = "0.0.0.0")
