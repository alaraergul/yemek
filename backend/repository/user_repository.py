from typing import Optional

from service.database_service import DatabaseService

from model.user import User, Language, Gender

class UserRepository:
  def __init__(self, db: DatabaseService):
    self.db = db

    self.db.get_cursor().execute(
      "CREATE TABLE IF NOT EXISTS users(" \
        "id uuid PRIMARY KEY DEFAULT gen_random_uuid()," \
        "username text UNIQUE NOT NULL," \
        "password text NOT NULL," \
        "firstname text NOT NULL," \
        "lastname text NOT NULL," \
        "purinelimit float," \
        "sugarlimit float," \
        "kcallimit float," \
        "weight int NOT NULL," \
        "gender bit NOT NULL," \
        "language bit NOT NULL"
      ");"
    )

    self.db.commit()

  def get_all_users(self):
    cur = self.db.get_cursor()
    cur.execute("SELECT id FROM users")
    response = cur.fetchall()
    return [value[0] for value in response]

  def get_user(self, id: str) -> User:
    cur = self.db.get_cursor()
    cur.execute("SELECT id, weight, gender, language, purinelimit, sugarlimit, kcallimit, firstname, lastname FROM users WHERE id=%s;", (id,))
    data = cur.fetchone()

    if data is None:
      return None
    else:
      return User(data[0], None, None, data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])

  def exists_user(self, username: str) -> bool:
    cur = self.db.get_cursor()
    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    data = cur.fetchone()

    return (data != None)

  def login(self, username: str, password: str) -> Optional[User]:
    cur = self.db.get_cursor()
    cur.execute(
      "SELECT id, weight, gender, language, purinelimit, sugarlimit, kcallimit, firstname, lastname FROM users WHERE username=%s AND password=%s;",
      (username, password)
    )

    user = cur.fetchone()

    if user == None:
      return None
    else:
      return User(user[0], None, None, user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8])

  def get_user_id(self, username: str, password: str) -> Optional[str]:
    cur = self.db.get_cursor()
    cur.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
    user_id = cur.fetchone()[0]

    return user_id

  def edit_user(self, id: str,
    gender: Gender, language: Language, weight: int, first_name: str, last_name: str,
    purine_limit: Optional[int], kcal_limit: Optional[int], sugar_limit: Optional[int]
  ) -> bool:
    cur = self.db.get_cursor()
    cur.execute(
      "UPDATE users SET gender=B'%s', weight=%s, language=B'%s', firstname=%s, lastname=%s, sugarlimit=%s, purinelimit=%s, kcallimit=%s WHERE id=%s;",
      (gender, weight, language, first_name, last_name, sugar_limit, purine_limit, kcal_limit, id)
    )

    self.db.commit()
    return cur.rowcount == 1

  def register(self, username: str, password: str, language: Language, gender: Gender, weight: int, first_name: str, last_name: str) -> str:
    cur = self.db.get_cursor()
    cur.execute(
      "INSERT INTO users(username, password, firstname, lastname, gender, weight, language) VALUES (%s, %s, %s, %s, B'%s', %s, B'%s') RETURNING id;",
      (username, password, first_name, last_name, gender, weight, language)
    )

    user_id = cur.fetchone()[0]
    self.db.commit()

    return user_id
