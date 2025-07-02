from flask import Flask, request
from firebase_admin import credentials, initialize_app, db
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
cred = credentials.Certificate("./firebase-key.json")
firebase = initialize_app(cred, {
  "databaseURL": getenv("FIREBASE_URL")
})

@app.route("/users/<int:user_id>", methods = ["POST"])
def post_meal(user_id):
  ref = db.reference(f"/{user_id}")
  ref.push(request.json)
  return ""

@app.route("/users/<int:user_id>", methods = ["GET"])
def get_meal(user_id):
  ref = db.reference(f"/{user_id}")
  data: dict = ref.get()
  return list(data.values())

@app.route("/users/<int:user_id>", methods = ["DELETE"])
def delete_meal(user_id):
  ref = db.reference(f"/{user_id}")
  data: dict = ref.get()
  new_data = dict()

  for key, value in data.items():
    if value["id"] != request.json["id"] or value["timestamp"] != request.json["timestamp"]:
      new_data[key] = value

  ref.set(new_data)
  return ""
