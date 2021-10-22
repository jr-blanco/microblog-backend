import configparser
import logging.config
from hug import authentication
import requests
import json

import hug
import sqlite_utils

# Load configuration
config = configparser.ConfigParser()
config.read("./etc/posts_api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# Arguements to inject into route functions
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
  dbfile = config[section][key]
  return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
  return logging.getLogger(name)


# Basic user verification for HTTP Basic Access Authentication
def user_verify(username, password):
  if username and password:
    r = requests.get(f"http://localhost:5000/users/search?username={username}&password={password}")
    data = r.json()['users']
    if r.status_code == 200 and data:
      return username
  return False

authentication = hug.authentication.basic(user_verify)

# Routes
#
# Home timeline
@hug.get("/timelines/home",
  examples=[
    "username=jblanco",
  ],
  requires=authentication,
  output=hug.output_format.pretty_json,
)
def home_timeline(request, db: sqlite, user:hug.directives.user):
  # get the users this user is following
  posts = []
  if "username" in request.params:
    r = requests.get(f"http://localhost:5000/following/{request.params['username']}")
    data = r.json()['following']

    for follower in data:
      posts.extend(list(db["posts"].rows_where("username = ?", [follower['friendname']])))
    
  return {"posts": posts}
      
      


# User timeline
@hug.get("/timelines/posts/{username}",
  output=hug.output_format.pretty_json
)
def user_timeline(db: sqlite, username: hug.types.text):
  return {"posts": db["posts"].rows_where("username = ?", [username], order_by="timestamp desc")}

# Public Timeline
@hug.get("/timelines/public",
  output=hug.output_format.pretty_json
)
def public_timeline(db: sqlite):
  return {"posts": db["posts"].rows_where(order_by="timestamp desc")}