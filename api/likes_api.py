import configparser
import logging.config
from hug import authentication
import requests
import json
import redis

import hug
import sqlite_utils

# Load configuration
config = configparser.ConfigParser()
config.read("./etc/posts_api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)
r = redis.Redis(host='localhost', port=6379, db=0)

# Arguements to inject into route functions
@hug.directive()
def sqlite(section="sqlite", key="dbfile", **kwargs):
  dbfile = config[section][key]
  return sqlite_utils.Database(dbfile)

@hug.directive()
def log(name=__name__, **kwargs):
  return logging.getLogger(name)

# Routes
#
# Get the number of likes of a post
@hug.get("/likes/{id}")
def get_likes(response, db: sqlite, id: hug.types.number):
  # get the users this user is following
  # r = redis.Redis(host='localhost', port=6379, db=0)
  if not r.exists(f"posts:{id}:likes"):
    response.status = hug.falcon.HTTP_404
  return {"likes": r.get(f"posts:{id}:likes")}

# Like a post by a certain amount
@hug.put("/likes/{id}", status=hug.falcon.HTTP_201)
def add_likes(
  response, 
  id: hug.types.number,
  amount: hug.types.number
  ):
  # r = redis.Redis(host='localhost', port=6379, db=0)
  r.incr(f'posts:{id}:likes', amount)

# list of users
