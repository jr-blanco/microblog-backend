import configparser
import logging.config

import hug
import requests
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

# gets all users
@json.get("/users/")
def users(db: sqlite):
  return {"users": db["users"].rows}

# create a new user
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

# retrieve a specific user
@json.get("/users/{id}")
def retrive_user(response, id: hug.types.number, db: sqlite):
  users = []
  try:
    user = db["users"].get(id)
    users.append(user)
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404
  return {"users": users}

# update a specific user
@json.put("/users/{id}", status=hug.falcon.HTTP_204)
def update_user(
  response,
  id: hug.types.number,
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
    users.get(id)
    users.update(id, user)
    user["id"] = users.last_pk
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404
  except Exception as e:
    response.status = hug.falcon.HTTP_409
    return {"error": str(e)}

# search for a user based off parameters
@json.get(
  "/users/search",
  examples=[
    "username=jblanco",
    "email=jrblanco@csu.fullerton.edu",
    "bio=living life",
    "password=pass"
  ],
)
def search(request, db: sqlite, logger: log):
  users = db["users"]

  conditions = []
  values = []

  if "username" in request.params:
    conditions.append("username = ?")
    values.append(request.params["username"])

  if "email" in request.params:
    conditions.append("email = ?")
    values.append(request.params["email"])

  if "bio" in request.params:
    conditions.append("bio LIKE ?")
    values.append(f"%{request.params['bio']}%")

  if "password" in request.params:
    conditions.append("password = ?")
    values.append(request.params['password'])

  if conditions:
    where = "AND ".join(conditions)
    logger.debug('WHERE "%s", %r', where, values)
    return {"users": users.rows_where(where, values)}
  else:
    return {"users": users}

# get a list of all followers
@json.get("/followers/")
def followers(db: sqlite):
  return {"followers": db["followers"].rows}

# create a new follower
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

# get a specific follower by resource id
@json.get("/followers/{id}")
def retrive_follower(response, id: hug.types.number, db: sqlite):
  followers = []
  try:
    followers = db["followers"].get(id)
    followers.append()
  except sqlite_utils.db.NotFoundError:
    response.status = hug.falcon.HTTP_404
  return {"followers": followers}

# search for follower ids based off parameters
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

# get a list of a usernames a user is following
@json.get(
  "/following/{username}",
)
def get_following(db: sqlite, username: hug.types.text):
  following = db["following"]
  return {"following": following.rows_where("username = ?", [username])}
