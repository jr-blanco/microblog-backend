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
@hug.get("/user/posts", requires=authentication)
def posts(db: sqlite, user:hug.directives.user):
  return {"posts": db["posts"].rows}