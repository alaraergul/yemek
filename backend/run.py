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
                "firstname text," \
                "lastname text," \
                "purinelimit float," \
                "sugarlimit float," \
                "kcallimit float," \
                "weight int NOT NULL," \
                "gender bit NOT NULL," \
                "language bit NOT NULL"
              ");")

  cur.execute("CREATE TABLE IF NOT EXISTS meals(" \
                "userid uuid references users(id)," \
                "id int NOT NULL," \
                "timestamp timestamp NOT NULL," \
                "count float NOT NULL"
              ");")

  cur.execute("CREATE TABLE IF NOT EXISTS custom_meals(" \
                "userid uuid references users(id)," \
                "id int NOT NULL," \
                "quantity int NOT NULL," \
                "purine float NOT NULL," \
                "sugar float NOT NULL," \
                "kcal float NOT NULL"
              ");")

  cur.execute("CREATE TABLE IF NOT EXISTS water_consumption(" \
                "user_id uuid references users(id)," \
                "value bit NOT NULL," \
                "timestamp timestamp NOT NULL"
              ");")
  conn.commit()
  return True

@app.route("/")
async def home():
  return render_template('index.html')


@app.route("/users/<user_id>/custom-meals", methods = ["GET"])
async def get_custom_meals(user_id):
  cur.execute("SELECT quantity, purine, sugar, kcal FROM custom_meals WHERE userid=%s", (user_id,))
  data = cur.fetchall()
  response = [{"quantity": meal[0], "purine": meal[1], "sugar": meal[2], "kcal": meal[3]} for meal in data]
  return {"success": True, "data": response}

@app.route("/users/<user_id>/custom-meals", methods = ["POST"])
async def add_custom_meal(user_id):
  cur.execute("INSERT INTO custom_meals (userid, quantity, purine, sugar, kcal) VALUES (%s, %s, %s, %s, %s)", (
    user_id, request.json["quantity"], request.json["purine"], request.json["sugar"], request.json["kcal"]
  ))
  conn.commit()
  return {"success": True}

@app.route("/meals/<user_id>", methods = ["GET"])
async def get_addable_meals(user_id):
  cur.execute("SELECT language FROM users WHERE id=%s", (user_id,))
  user_language_row = cur.fetchone()
  if not user_language_row:
      return {"success": False, "message": "User not found"}, 404
  language = int(user_language_row[0])

  data = []
  for category in categories:
    meals = [{
      "id": meal["id"], "name": meal["names"][language], "purine": meal["purine"],
      "kcal": meal["kcal"], "quantity": meal["quantity"], "sugar": meal["sugar"]
    } for meal in category["meals"]]
    data.append({"name": category["names"][language], "meals": meals})
  return {"success": True, "data": data}


@app.route("/users/<user_id>/water-consumption", methods = ["GET"])
async def get_water_consumption(user_id):
  cur.execute("SELECT value, extract(epoch from timestamp) FROM water_consumption WHERE user_id=%s;", (user_id,))
  water_consumption = cur.fetchall()
  response = [{"value": int(data[0]), "timestamp": int(data[1]) * 1000} for data in water_consumption]
  return {"success": True, "data": response}

@app.route("/users/<user_id>/water-consumption", methods = ["POST"])
async def post_water_consumption(user_id):
  cur.execute(
    "INSERT INTO water_consumption (user_id, value, timestamp) VALUES (%s, B'%s', to_timestamp(%s))",
    (user_id, request.json["value"], request.json["timestamp"] / 1000)
  )
  conn.commit()
  return {"success": True}



@app.route("/users/<user_id>/meals", methods = ["GET"])
async def get_meals(user_id):
  cur.execute("SELECT id, count, extract(epoch from timestamp) FROM meals WHERE userid=%s;", (user_id,))
  meals = cur.fetchall()
  response = [{"id": meal[0], "count": meal[1], "timestamp": int(meal[2]) * 1000} for meal in meals]
  return {"success": True, "data": response}

@app.route("/users/<user_id>/meals", methods = ["POST"])
async def post_meal(user_id):
  args = b",".join(cur.mogrify("(%s, %s, to_timestamp(%s), %s)", (user_id, data["id"], data["timestamp"] / 1000, data["count"])) for data in request.json).decode("utf-8")
  cur.execute(f"INSERT INTO meals (userid, id, timestamp, count) VALUES {args}")
  conn.commit()
  return {"success": True}

@app.route("/users/<user_id>/meals", methods = ["DELETE"])
async def delete_meal(user_id):
  cur.execute("DELETE FROM meals WHERE userid=%s AND id=%s AND timestamp=to_timestamp(%s);", (user_id, request.json["id"], request.json["timestamp"] / 1000))
  conn.commit()
  return {"success": True}



@app.route("/users", methods = ["GET"])
async def get_users():
  cur.execute("SELECT id FROM users")
  response = cur.fetchall()
  return [value[0] for value in response]

@app.route("/users/<user_id>", methods = ["GET"])
async def get_user(user_id):
  cur.execute("SELECT id, purinelimit, kcallimit, sugarlimit, weight, gender, language, firstname, lastname FROM users WHERE id=%s;", (user_id,))
  user = cur.fetchone()

  if user is None:
    return {"success": False, "message": "There is no user."}, 404
  else:
    return {"success": True, "data": {
      "id": user[0], "purineLimit": user[1], "kcalLimit": user[2], "sugarLimit": user[3], "weight": user[4], "gender": int(user[5]), "language": int(user[6]),
      "firstname": user[7], "lastname": user[8]
    }}

@app.route("/users/<user_id>", methods = ["PATCH"])
async def edit_user(user_id):
  cur.execute("SELECT username, password FROM users WHERE id=%s;", (user_id,))
  db_user = cur.fetchone()

  if db_user is None or db_user[1] != request.json["password"] or db_user[0] != request.json["username"]:
      return {"success": False, "message": "Username or password do not match."}, 403

  cur.execute("UPDATE users SET gender=B'%s', weight=%s, language=B'%s', sugarlimit=%s, purinelimit=%s, kcallimit=%s WHERE id=%s;", (
    request.json.get("gender"), request.json.get("weight"), request.json.get("language"),
    request.json.get("sugarLimit"), request.json.get("purineLimit"), request.json.get("kcalLimit"),
    user_id
  ))
  conn.commit()
  return {"success": True}

@app.route("/users/register", methods = ["POST"])
async def create_new_user():
  cur.execute("SELECT id FROM users WHERE username=%s", (request.json["username"],))
  if cur.fetchone() is not None:
    return {"success": False, "message": "This user already exists."}, 403

  cur.execute("INSERT INTO users(username, password, firstname, lastname, gender, weight, language) VALUES (%s, %s, %s, %s, B'%s', %s, B'%s') RETURNING id;", (
    request.json["username"], request.json["password"], request.json["firstname"], request.json["lastname"], request.json["gender"], request.json["weight"], request.json["language"]
  ))
  user_id = cur.fetchone()[0]
  conn.commit()

  return {"success": True, "data": {
    "id": user_id, "weight": request.json["weight"], "gender": request.json["gender"], "language": request.json["language"],
    "firstname": request.json["firstname"], "lastname": request.json["lastname"]
  }}

@app.route("/users/login", methods = ["POST"])
async def check_user_credientals():
  cur.execute("SELECT id, weight, gender, purinelimit, sugarlimit, kcallimit, language, firstname, lastname FROM users WHERE username=%s AND password=%s;", (
    request.json["username"], request.json["password"]
  ))
  user = cur.fetchone()

  if user is None:
    return {"success": False, "message": "Wrong credientals"}, 403

  return {"success": True, "data": {
    "id": user[0], "weight": user[1], "gender": int(user[2]),
    "purineLimit": user[3], "sugarLimit": user[4], "kcalLimit": user[5], "language": int(user[6]),
    "firstname": user[7], "lastname": user[8]
  }}

if __name__ == "__main__":
  create_database_tables()
  app.run(port = 8087, host = "0.0.0.0", debug=True)