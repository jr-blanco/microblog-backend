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
json = hug.get(output=hug.output_format.pretty_json)

@json.get("/users/")
def users(db: sqlite):
  return {"users": db["users"].rows}

@json.post("/users/", status=hug.falcon.HTTP_201)
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

@json.get("/users/{id}")
def retrive_user(response, id: hug.types.number, db: sqlite):
  users = []
  try:
    user = db["users"].get(id)
    users.append(user)
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404
  return {"users": users}

@json.get(
  "/users/search",
  examples=[
    "username=jblanco",
    "email=jrblanco@csu.fullerton.edu",
    "bio=living life",
  ],
)
def search(request, db: sqlite, logger: log):
  users = db["users"]

  conditions = []
  values = []

  for column in ["username", "email", "bio"]:
    if column in request.params:
      conditions.append(f"{column} LIKE ?")
      values.append(f"%{request.params[column]}%")

  if conditions:
    where = "AND ".join(conditions)
    logger.debug('WHERE "%s", %r', where, values)
    return {"users": users.rows_where(where, values)}
  else:
    return {"users": users.rows}

@json.get("/followers/")
def followers(db: sqlite):
  return {"followers": db["followers"].rows}

@json.post("/followers/", status=hug.falcon.HTTP_201)
def create_follower(
  response,
  follower_id: hug.types.number,
  following_id: hug.types.number,
  db: sqlite,
):
  followers = db["followers"]

  follower = {
    "follower_id": follower_id,
    "following_id": following_id,
  }

  try:
    followers.insert(follower)
    follower["id"] = followers.last_pk
  except Exception as e:
    response.status = hug.falcon.HTTP_409
    return {"error": str(e)}

  response.set_header("Location", f"/followers/{follower['id']}")
  return follower

@json.get("/followers/{id}")
def retrive_follower(response, id: hug.types.number, db: sqlite):
  followers = []
  try:
    followers = db["followers"].get(id)
    followers.append()
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404
  return {"followers": followers}

@json.get("/users/{id}/followers/")
def retrieve_followers(response, id: hug.types.number, db: sqlite):
  followers = []
  try:
    db["users"].get(id)
    for row in db["followers"].rows_where("follower_id = ?", [id]):
      followers.append(row)
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404

  return {"followers": followers}

@json.get(
  "/followers/search",
  examples=[
    "follower_id=1",
    "following_id=3",
  ],
)
def search(request, db: sqlite, logger: log):
  followers = db["followers"]

  conditions = []
  values = []

  if "follower_id" in request.params:
    conditions.append("follower_id = ?")
    values.append(request.params["follower_id"])

  if "following_id" in request.params:
    conditions.append("following_id = ?")
    values.append(request.params["following_id"])

  if conditions:
    where = "AND ".join(conditions)
    logger.debug('WHERE "%s", %r', where, values)
    return {"followers": followers.rows_where(where, values)}
  else:
    return {"followers": followers.rows}

@json.get("/following/")
def followers(db: sqlite):
  return {"following": db["following"].rows}

@json.get(
  "/following/search",
  examples=[
    "username=jbestwall2l",
    "friendname=hleagast",
  ],
)
def search(request, db: sqlite, logger: log):
  following = db["following"]

  conditions = []
  values = []

  if "username" in request.params:
    conditions.append("username = ?")
    values.append(request.params["username"])

  if "friendname" in request.params:
    conditions.append("friendname = ?")
    values.append(request.params["friendname"])

  if conditions:
    where = "AND ".join(conditions)
    logger.debug('WHERE "%s", %r', where, values)
    return {"following": following.rows_where(where, values)}
  else:
    return {"following": following.rows}
