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
@hug.get("/likes/{post_id}")
def get_likes(response, db: sqlite, post_id: hug.types.number):
  # get the users this user is following
  if not r.exists(f"posts:{post_id}:likes"):
    response.status = hug.falcon.HTTP_404
  return {"likes": r.get(f"posts:{post_id}:likes")}

# Like a post by a certain amount
# TODO: check if user has already like post
@hug.put("/likes/{post_id}", status=hug.falcon.HTTP_201)
def add_likes(
  response, 
  post_id: hug.types.number,
  user_id: hug.types.number,
  amount: hug.types.number
  ):
  r.incr(f'posts:{post_id}:likes', amount)
  r.rpush(f'users:{user_id}:likes', post_id)
  num = r.get(f'posts:{post_id}:likes')
  r.zadd('leaderboard', {post_id: num})

# list of users' likes
@hug.get("/likes/users/{user_id}")
def get_user_likes(
  response,
  user_id: hug.types.number
):
  if not r.exists(f"users:{user_id}:likes"):
    response.status = hug.falcon.HTTP_404
  return {"likes": r.lrange(f"likes:{user_id}:list", 0, -1)}

# return list of top 10 popular posts
@hug.get("/likes/popular")
def get_popular(response):
  return {"likes": r.zrevrange('leaderboard', 0, 10)}
