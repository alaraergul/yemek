from flask import Flask, request, Request, render_template
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
from os import getenv
from data_file import categories

load_dotenv()
conn = psycopg2.connect(database=getenv("DATABASE_NAME"), user=getenv("DATABASE_USER"), password=getenv("DATABASE_PASS"), host=getenv("DATABASE_HOST"))
cur = conn.cursor()

app = Flask(__name__)
CORS(app)

def create_database_tables():
  cur.execute("CREATE TABLE IF NOT EXISTS users(" \
                "id uuid PRIMARY KEY DEFAULT gen_random_uuid()," \
                "username text UNIQUE NOT NULL," \
                "password text NOT NULL," \
                "purine_limit float," \
                "sugar_limit float," \
                "kcal_limit float," \
                "weight int NOT NULL," \
                "gender bit NOT NULL," \
                "language bit NOT NULL"
              ");")

  cur.execute("CREATE TABLE IF NOT EXISTS meals(" \
                "user_id uuid references users(id)," \
                "id int NOT NULL," \
                "timestamp timestamp NOT NULL," \
                "count float NOT NULL"
              ");")

  cur.execute("CREATE TABLE IF NOT EXISTS custom_meals(" \
                "user_id uuid references users(id)," \
                "id int NOT NULL," \
                "quantity int NOT NULL," \
                "purine float NOT NULL," \
                "sugar float NOT NULL," \
                "kcal float NOT NULL"
              ");")

  cur.execute("CREATE TABLE IF NOT EXISTS water_consumption(" \
                "user_id uuid references Users(id)," \
                "value bit NOT NULL," \
                "timestamp timestamp NOT NULL"
              ");")

  conn.commit()

  return True

create_database_tables()

@app.route("/")
async def home():
  return render_template('index.html')


@app.route("/users/<user_id>/custom-meals", methods = ["GET"])
async def get_custom_meals(user_id):
  cur.execute("SELECT quantity, purine, sugar, kcal WHERE user_id=%s", (user_id,))
  data = cur.fetchall()

  if len(data) == 0:
    return list()
  else:
    response = []

    for meal in data:
      response.append({"quantity": meal[0], "purine": meal[1], "sugar": meal[2], "kcal": meal[3]})

    return {"success": True, "data": response}

@app.route("/users/<user_id>/custom-meals", methods = ["POST"])
async def add_custom_meal(user_id):
  if not "quantity" in request.json or not isinstance(request.json["quantity"], float):
    return {"success": False, "message": "Body must contain \"quantity\" key and it must be a float."}, 400

  if not "purine" in request.json or not isinstance(request.json["purine"], float):
    return {"success": False, "message": "Body must contain \"timestamp\" key and it must be a float."}, 400

  if not "sugar" in request.json or not isinstance(request.json["sugar"], float):
    return {"success": False, "message": "Body must contain \"sugar\" key and it must be a float."}, 400

  if not "kcal" in request.json or not isinstance(request.json["kcal"], float):
    return {"success": False, "message": "Body must contain \"kcal\" key and it must be a float."}, 400

  cur.execute("INSERT INTO user_id, quantity, purine, sugar, kcal VALUES (%s, %s, %s, %s, %s)", (
    user_id, request.json["quantity"], request.json["purine"], request.json["sugar"], request.json["kcal"]
  ))
  conn.commit()

  return {"success": True}

@app.route("/meals/<user_id>", methods = ["GET"])
async def get_addable_meals(user_id):
  cur.execute("SELECT language FROM users WHERE id=%s", (user_id,))
  language = int(cur.fetchone()[0])

  data = []

  for category in categories:
    meals = []

    for meal in category["meals"]:
      meals.append({
        "id": meal["id"],
        "name": meal["names"][language],
        "purine": meal["purine"],
        "kcal": meal["kcal"],
        "quantity": meal["quantity"],
        "sugar": meal["sugar"]
      })

    data.append({
      "name": category["names"][language],
      "meals": meals
    })

  return {"success": True, "data": data}


@app.route("/users/<user_id>/water-consumption", methods = ["GET"])
async def get_water_consumption(user_id):
  cur.execute("SELECT value, extract(epoch from timestamp) FROM water_consumption WHERE user_id=%s;", (user_id,))
  water_consumption = cur.fetchall()

  if len(water_consumption) == 0:
    return list()
  else:
    response = []

    for data in water_consumption:
      response.append({"value": data[0], "timestamp": int(data[1]) * 1000})

    return {"success": True, "data": response}

@app.route("/users/<user_id>/water-consumption", methods = ["POST"])
async def post_water_consumption(user_id):
  if not "value" in request.json or not isinstance(request.json["value"], int):
    return {"success": False, "message": "Body must contain \"value\" key and it must be a number."}, 400

  if not "timestamp" in request.json or not isinstance(request.json["timestamp"], int):
    return {"success": False, "message": "Body must contain \"timestamp\" key and it must be a number that represents unix timestamp."}, 400

  cur.execute(
    "INSERT INTO WaterConsumption (user_id, value, timestamp) VALUES (%s, B'%s', to_timestamp(%s))",
    (user_id, request.json["value"], request.json["timestamp"] / 1000)
  )

  conn.commit()

  return {"success": True}



@app.route("/users/<user_id>/meals", methods = ["GET"])
async def get_meals(user_id):
  cur.execute("SELECT id, count, extract(epoch from timestamp) FROM meals WHERE user_id=%s;", (user_id,))
  meals = cur.fetchall()

  if len(meals) == 0:
    return {"success": True, "data": list()}
  else:
    response = []

    for meal in meals:
      response.append({"id": meal[0], "count": meal[1], "timestamp": int(meal[2]) * 1000})

    return {"success": True, "data": response}

@app.route("/users/<user_id>/meals", methods = ["POST"])
async def post_meal(user_id):
  if not isinstance(request.json, list):
    return {"success": False, "message": "Body must be a list."}, 400

  for data in request.json:
    if not "id" in data or not isinstance(data["id"], int):
      return {"success": False, "message": "Data must contain \"id\" key and it must be a number."}, 400

    if not "count" in data or (not isinstance(data["count"], float) and not isinstance(data["count"], int)):
      return {"success": False, "message": "Data must contain \"count\" key and it must be a number."}, 400

    if not "timestamp" in data or not isinstance(data["timestamp"], int):
      return {"success": False, "message": "Data must contain \"timestamp\" key and it must be a number that represents unix timestamp."}, 400

  args = b",".join(cur.mogrify("(%s, %s, to_timestamp(%s), %s)", (user_id, data["id"], data["timestamp"] / 1000, data["count"])) for data in request.json).decode("utf-8")

  cur.execute(f"INSERT INTO Meals (user_id, id, timestamp, count) VALUES {args}")
  conn.commit()

  return {"success": True}

@app.route("/users/<user_id>/meals", methods = ["DELETE"])
async def delete_meal(user_id):
  if not "id" in request.json or not isinstance(request.json["id"], int):
    return {"success": False, "message": "Body must contain \"id\" key and it must be a number."}, 400

  if not "timestamp" in request.json or not isinstance(request.json["timestamp"], int):
    return {"success": False, "message": "Body must contain \"timestamp\" key and it must be a number that represents unix timestamp."}, 400

  cur.execute("DELETE FROM Meals WHERE user_id=%s AND id=%s AND timestamp=to_timestamp(%s);", (user_id, request.json["id"], request.json["timestamp"] / 1000))
  conn.commit()

  return {"success": True}



@app.route("/users", methods = ["GET"])
async def get_users():
  cur.execute("SELECT id FROM users")
  response = cur.fetchall()

  return list(map(lambda value: value[0], response))

@app.route("/users/<user_id>", methods = ["GET"])
async def get_user(user_id):
  cur.execute("SELECT id, purine_limit, kcal_limit, sugar_limit, weight, gender, language FROM users WHERE id=%s;", (user_id,))
  user = cur.fetchone()

  if user == None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    return {"success": True, "data": {
      "id": user[0], "purineLimit": user[1], "kcalLimit": user[2], "sugarLimit": user[3], "weight": user[4], "gender": int(user[5]), "language": int(user[6])
    }}

@app.route("/users/<user_id>", methods = ["PATCH"])
async def edit_user(user_id):
  cur.execute("SELECT username, password, weight, gender, purine_limit, sugar_limit, kcal_limit, language FROM users WHERE id=%s;", (user_id,))
  user = cur.fetchone()

  if not ("password" in request.json and isinstance(request.json["password"], str)) or not ("username" in request.json and isinstance(request.json["username"], str)):
    return {"success": False, "message": "Username and password must be existed."}, 403

  if user == None or user[1] != request.json["password"] or user[0] != request.json["username"]:
    return {"success": False, "message": "Username or password do not match."}, 403

  data = {
    "weight": user[2],
    "gender": user[3],
    "purine_limit": user[4],
    "sugar_limit": user[5],
    "kcal_limit": user[6],
    "language": user[7]
  }

  if "weight" in request.json and isinstance(request.json["weight"], float):
    data["weight"] = request.json["weight"]

  if "purine_limit" in request.json:
    if isinstance(request.json["purine_limit"], float):
      data["purine_limit"] = request.json["purine_limit"]
    elif request.json["purine_limit"] == None and "purine_limit" in data:
      data["purine_limit"] = None

  if "sugar_limit" in request.json:
    if isinstance(request.json["sugar_limit"], float):
      data["sugar_limit"] = request.json["sugar_limit"]
    elif request.json["sugar_limit"] == None and "sugar_limit" in data:
      data["sugar_limit"] = None

  if "kcal_limit" in request.json:
    if isinstance(request.json["kcal_limit"], float):
      data["kcal_limit"] = request.json["kcal_limit"]
    elif request.json["kcal_limit"] == None and "kcal_limit" in data:
      data["kcal_limit"] = None

  if "gender" in request.json and isinstance(request.json["gender"], int):
    data["gender"] = request.json["gender"]

  if "language" in request.json and isinstance(request.json["language"], int):
    data["language"] = request.json["language"]

  cur.execute("UPDATE users SET gender=B'%s', weight=%s, language=B'%s', sugar_limit=%s, purine_limit=%s, kcal_limit=%s WHERE id=%s;", (
    data["gender"], data["weight"], data["language"], data["sugar_limit"], data["purine_limit"], data["kcal_limit"], user_id
  ))
  conn.commit()

  return {"success": True}

@app.route("/users/register", methods = ["POST"])
async def create_new_user():
  if not "username" in request.json or not isinstance(request.json["username"], str):
    return {"success": False, "message": "Body must contain \"username\" key and it must be a string."}, 400

  if not "password" in request.json or not isinstance(request.json["password"], str):
    return {"success": False, "message": "Body must contain \"password\" key and it must be a string."}, 400

  if not "weight" in request.json or not isinstance(request.json["weight"], int):
    return {"success": False, "message": "Body must contain \"weight\" key and it must be a number."}, 400

  if not "gender" in request.json or not isinstance(request.json["gender"], int):
    return {"success": False, "message": "Body must contain \"gender\" key and it must be a number."}, 400

  if not "language" in request.json or not isinstance(request.json["language"], int):
    return {"success": False, "message": "Body must contain \"language\" key and it must be a number."}, 400

  cur.execute("SELECT id FROM users WHERE username=%s", (request.json["username"],))

  if cur.fetchone() != None:
    return {"success": False, "message": "This user already exists."}, 403

  cur.execute("INSERT INTO users(username, password, gender, weight, language) VALUES (%s, %s, B'%s', %s, B'%s') RETURNING id;", (
    request.json["username"], request.json["password"], request.json["gender"], request.json["weight"], request.json["language"]
  ))

  conn.commit()

  return {"success": True, "data": {
    "id": cur.fetchone()[0], "weight": request.json["weight"], "gender": request.json["gender"], "language": request.json["language"]
  }}

@app.route("/users/login", methods = ["POST"])
async def check_user_credientals():
  if not "username" in request.json or not isinstance(request.json["username"], str):
    return {"success": False, "message": "Body must contain \"username\" key and it must be a string."}, 400

  if not "password" in request.json or not isinstance(request.json["password"], str):
    return {"success": False, "message": "Body must contain \"password\" key and it must be a string."}, 400

  cur.execute("SELECT COUNT(*) FROM Users")
  count = cur.fetchone()[0]

  if count == 0:
    return {"success": False, "message": "There is no user"}, 404

  cur.execute("SELECT id, weight, gender, purine_limit, sugar_limit, kcal_limit, language FROM Users WHERE username=%s AND password=%s;", (
    request.json["username"], request.json["password"]
  ))

  user = cur.fetchone()

  if user == None:
    return {"success": False, "message": "Wrong credientals"}, 403

  return {"success": True, "data": {
    "id": user[0], "weight": user[1], "gender": int(user[2]), "purine_limit": user[3], "sugar_limit": user[4], "kcal_limit": user[5], "language": user[6]
  }}

if __name__ == "__main__":
  app.run(port = 8087, host = "0.0.0.0")
