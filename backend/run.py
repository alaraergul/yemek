from flask import Flask, request, Request, render_template
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
from os import getenv

load_dotenv()
conn = psycopg2.connect(database=getenv("DATABASE_NAME"), user=getenv("DATABASE_USER"), password=getenv("DATABASE_PASS"), host=getenv("DATABASE_HOST"))
cur = conn.cursor()

app = Flask(__name__)
CORS(app)


cur.execute("CREATE TABLE IF NOT EXISTS Users(" \
              "id uuid PRIMARY KEY DEFAULT gen_random_uuid()," \
              "username text UNIQUE NOT NULL," \
              "password text NOT NULL," \
              "purineLimit int," \
              "sugarLimit int," \
              "kcalLimit int," \
              "weight int NOT NULL," \
              "gender bit NOT NULL" \
            ");")

cur.execute("CREATE TABLE IF NOT EXISTS Meals(" \
              "userId uuid references Users(id)," \
              "id int NOT NULL," \
              "timestamp timestamp NOT NULL," \
              "count int NOT NULL"
            ");")

cur.execute("CREATE TABLE IF NOT EXISTS WaterConsumption(" \
              "userId uuid references Users(id)," \
              "value bit NOT NULL," \
              "timestamp timestamp NOT NULL"
            ");")

conn.commit()


def check_is_valid_request(data: Request, element_count: int):
  if not data.is_json or not isinstance(data.json, dict):
    return {"code": 400, "message": "Body must be a JSON object."}

  if len(data.json) != element_count:
    return {"code": 400, "message": f"Body must contain exactly {element_count} members."}

  return True

def check_is_valid_data(data: dict, element_count: int):
  if not isinstance(data, dict):
    return {"code": 400, "message": "Body must be a JSON object."}

  if len(data) != element_count:
    return {"code": 400, "message": f"Body must contain exactly {element_count} members."}

  return True


@app.route("/")
def home():
  return render_template('index.html')

@app.route("/users/<user_id>/water_consumption", methods = ["POST"])
def post_water_consumption(user_id):
  if (error := check_is_valid_request(request, 2)) != True:
    return error

  if not "value" in request.json or not isinstance(request.json["value"], int):
    return {"code": 400, "message": "Body must contain \"value\" key and it must be a number."}

  if not "timestamp" in request.json or not isinstance(request.json["timestamp"], int):
    return {"code": 400, "message": "Body must contain \"timestamp\" key and it must be a number that represents unix timestamp."}

  cur.execute(
    "INSERT INTO WaterConsumption (userId, value, timestamp) VALUES (%s, B'%s', to_timestamp(%s))",
    (user_id, request.json["value"], request.json["timestamp"] / 1000)
  )

  conn.commit()

  return ""

@app.route("/users/<user_id>/water_consumption", methods = ["GET"])
def get_water_consumption(user_id):
  cur.execute("SELECT value, extract(epoch from timestamp) FROM WaterConsumption WHERE userId=%s;", (user_id,))
  water_consumption = cur.fetchall()

  if len(water_consumption) == 0:
    return list()
  else:
    response = []

    for data in water_consumption:
      response.append({"value": data[0], "timestamp": int(data[1]) * 1000})

    return response

@app.route("/users/<user_id>/meals", methods = ["POST"])
def post_meal(user_id):
  if not isinstance(request.json, list):
    return {"code": 400, "message": "Body must be a list."}

  for data in request.json:
    if (error := check_is_valid_data(data, 3)) != True:
      return error

    if not "id" in data or not isinstance(data["id"], int):
      return {"code": 400, "message": "Data must contain \"id\" key and it must be a number."}

    if not "count" in data or not isinstance(data["count"], int):
      return {"code": 400, "message": "Data must contain \"count\" key and it must be a number."}

    if not "timestamp" in data or not isinstance(data["timestamp"], int):
      return {"code": 400, "message": "Data must contain \"timestamp\" key and it must be a number that represents unix timestamp."}

  args = b",".join(cur.mogrify("(%s, %s, to_timestamp(%s), %s)", (user_id, data["id"], data["timestamp"] / 1000, data["count"])) for data in request.json).decode("utf-8")

  cur.execute(f"INSERT INTO Meals (userId, id, timestamp, count) VALUES {args}")
  conn.commit()

  return ""

@app.route("/users/<user_id>/meals", methods = ["GET"])
def get_meals(user_id):
  cur.execute("SELECT id, count, extract(epoch from timestamp) FROM Meals WHERE userId=%s;", (user_id,))
  meals = cur.fetchall()

  if len(meals) == 0:
    return list()
  else:
    response = []

    for meal in meals:
      response.append({"id": meal[0], "count": meal[1], "timestamp": int(meal[2]) * 1000})

    return response

@app.route("/users/<user_id>/meals", methods = ["DELETE"])
def delete_meal(user_id):
  if (error := check_is_valid_request(request, 2)) != True:
    return error

  if not "id" in request.json or not isinstance(request.json["id"], int):
    return {"code": 400, "message": "Body must contain \"id\" key and it must be a number."}

  if not "timestamp" in request.json or not isinstance(request.json["timestamp"], int):
    return {"code": 400, "message": "Body must contain \"timestamp\" key and it must be a number that represents unix timestamp."}

  cur.execute("DELETE FROM Meals WHERE userId=%s AND id=%s AND timestamp=to_timestamp(%s);", (user_id, request.json["id"], request.json["timestamp"] / 1000))
  conn.commit()

  return ""

@app.route("/users", methods = ["GET"])
def get_users():
  cur.execute("SELECT id FROM Users")
  response = cur.fetchall()

  return list(map(lambda value: value[0], response))

@app.route("/users/<user_id>", methods = ["GET"])
def get_user(user_id):
  cur.execute("SELECT id, purineLimit, kcalLimit, sugarLimit, weight, gender FROM Users WHERE id=%s;", (user_id,))
  user = cur.fetchone()

  if user == None:
    return {"code": 404, "message": "There is no user."}
  else:
    return {"id": user[0], "purineLimit": user[1], "kcalLimit": user[2], "sugarLimit": user[3], "weight": user[4], "gender": int(user[5])}

@app.route("/users/<user_id>", methods = ["PATCH"])
def edit_user(user_id):
  cur.execute("SELECT username, password, weight, gender, purineLimit, sugarLimit, kcalLimit FROM Users WHERE id=%s;", (user_id,))
  user = cur.fetchone()

  if not ("password" in request.json and isinstance(request.json["password"], str)) or not ("username" in request.json and isinstance(request.json["username"], str)):
    return {"code": 403, "message": "Username and password must be existed."}

  if user == None or user[1] != request.json["password"] or user[0] != request.json["username"]:
    return {"code": 403, "message": "Username or password do not match."}

  data = {
    "weight": user[2],
    "gender": user[3],
    "purineLimit": user[4],
    "sugarLimit": user[5],
    "kcalLimit": user[6]
  }

  if "weight" in request.json and isinstance(request.json["weight"], int):
    data["weight"] = request.json["weight"]

  if "purineLimit" in request.json:
    if isinstance(request.json["purineLimit"], int):
      data["purineLimit"] = request.json["purineLimit"]
    elif request.json["purineLimit"] == None and "purineLimit" in data:
      data["purineLimit"] = None

  if "sugarLimit" in request.json:
    if isinstance(request.json["sugarLimit"], int):
      data["sugarLimit"] = request.json["sugarLimit"]
    elif request.json["sugarLimit"] == None and "sugarLimit" in data:
      data["sugarLimit"] = None

  if "kcalLimit" in request.json:
    if isinstance(request.json["kcalLimit"], int):
      data["kcalLimit"] = request.json["kcalLimit"]
    elif request.json["kcalLimit"] == None and "kcalLimit" in data:
      data["kcalLimit"] = None

  if "gender" in request.json and isinstance(request.json["gender"], int):
    data["gender"] = request.json["gender"]

  cur.execute("UPDATE Users SET gender=B'%s', weight=%s, sugarLimit=%s, purineLimit=%s, kcalLimit=%s WHERE id=%s;", (
    data["gender"], data["weight"], data["sugarLimit"], data["purineLimit"], data["kcalLimit"], user_id
  ))
  conn.commit()

  return ""

@app.route("/users/register", methods = ["POST"])
def create_new_user():
  if (error := check_is_valid_request(request, 4)) != True:
    return error

  if not "username" in request.json or not isinstance(request.json["username"], str):
    return {"code": 400, "message": "Body must contain \"username\" key and it must be a string."}

  if not "password" in request.json or not isinstance(request.json["password"], str):
    return {"code": 400, "message": "Body must contain \"password\" key and it must be a string."}

  if not "weight" in request.json or not isinstance(request.json["weight"], int):
    return {"code": 400, "message": "Body must contain \"weight\" key and it must be a number."}

  if not "gender" in request.json or not isinstance(request.json["gender"], int):
    return {"code": 400, "message": "Body must contain \"gender\" key and it must be a number."}

  cur.execute("SELECT id FROM Users WHERE username=%s", (request.json["username"],))

  if cur.fetchone() != None:
    return {"code": 403, "message": "This user already exists."}

  cur.execute("INSERT INTO Users(username, password, gender, weight) VALUES (%s, %s, B'%s', %s) RETURNING id;", (
    request.json["username"], request.json["password"], request.json["gender"], request.json["weight"]
  ))

  conn.commit()

  return {"id": cur.fetchone()[0], "weight": request.json["weight"], "gender": request.json["gender"]}

@app.route("/users/login", methods = ["POST"])
def check_user_credientals():
  if (error := check_is_valid_request(request, 2)) != True:
    return error

  if not "username" in request.json or not isinstance(request.json["username"], str):
    return {"code": 400, "message": "Body must contain \"username\" key and it must be a string."}

  if not "password" in request.json or not isinstance(request.json["password"], str):
    return {"code": 400, "message": "Body must contain \"password\" key and it must be a string."}

  cur.execute("SELECT COUNT(*) FROM Users")
  count = cur.fetchone()[0]

  if count == 0:
    return {"code": 404, "message": "There is no user"}

  cur.execute("SELECT id, weight, gender, purineLimit, sugarLimit, kcalLimit FROM Users WHERE username=%s AND password=%s;", (
    request.json["username"], request.json["password"]
  ))

  user = cur.fetchone()

  if user == None:
    return {"code": 403, "message": "Wrong credientals"}

  return {"id": user[0], "weight": user[1], "gender": int(user[2]), "purineLimit": user[3], "sugarLimit": user[4], "kcalLimit": user[5]}

if __name__ == "__main__":
  app.run(port = 8087, host = "0.0.0.0")
