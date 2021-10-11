import configparser
import logging.config

import hug
import sqlite_utils

# Load configuration
config = configparser.ConfigParser()
config.read("./etc/users_api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# Arguements to inject into route functions
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
  dbfile = config[section][key]
  return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
  return logging.getLogger(name)

# Routes
@hug.get("/users/")
def users(db: sqlite):
  return {"users": db["users"].rows}

@hug.post("/users/", status=hug.falcon.HTTP_201)
def create_user(
  response,
  username: hug.types.text,
  email: hug.types.text,
  bio: hug.types.text,
  password: hug.types.text,
  db: sqlite,
):
  users = db["users"]

  user = {
    "username": username,
    "email": email,
    "bio": bio,
    "password": password,
  }

  try:
    users.insert(user)
    user["id"] = users.last_pk
  except Exception as e:
    response.status = hug.falcon.HTTP_409
    return {"error": str(e)}

  response.set_header("Location", f"/users/{user['id']}")
  return user

@hug.get("/users/{id}")
def retrive_user(response, id: hug.types.number, db: sqlite):
  users = []
  try:
    user = db["users"].get(id)
    users.append(user)
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404
  return {"users": users}

# @hug.get(
#   "/search",
#   examples=[
#     "username=jblanco",
#     "email=jrblanco@csu.fullerton.edu",
#     "bio=living life",
#   ],
# )
# def search(request, db: sqlite, logger: log):
#   users = db["users"]

#   conditions = []
#   values = []

#   if "username" in request.params:
#     conditions.append("username = ?")