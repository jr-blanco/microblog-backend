import configparser
import logging.config
import redis

import hug


# Load configuration
config = configparser.ConfigParser()
config.read("./etc/likes_api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# Arguements to inject into route functions
@hug.directive()
def _redis(dbPort=6379, dbValue=0, **kwargs):
  return redis.Redis(host='localhost', port=dbPort, db=dbValue)

@hug.directive()
def log(name=__name__, **kwargs):
  return logging.getLogger(name)

# Routes
#
# Get the number of likes of a post
@hug.get("/likes/{post_id}")
def get_likes(response, db: _redis, post_id: hug.types.number, output=hug.output_format.pretty_json):
  # get the users this user is following
  if not db.exists(f"posts:{post_id}:likes"):
    response.status = hug.falcon.HTTP_404
  return {"likes": db.get(f"posts:{post_id}:likes")}

# Like a post by a certain amount
# TODO: check if user has already like post
@hug.put("/likes/{post_id}", status=hug.falcon.HTTP_201)
def add_likes(
  response, 
  post_id: hug.types.number,
  user_id: hug.types.number,
  amount: hug.types.number,
  db: _redis
  ):
  db.incr(f'posts:{post_id}:likes', amount)
  db.rpush(f'users:{user_id}:likes', post_id)
  num = db.get(f'posts:{post_id}:likes')
  db.zadd('leaderboard', {post_id: num})

# list of users' likes
@hug.get("/likes/users/{user_id}", output=hug.output_format.pretty_json)
def get_user_likes(
  response,
  user_id: hug.types.number,
  db: _redis
):
  if not db.exists(f"users:{user_id}:likes"):
    response.status = hug.falcon.HTTP_404
  return {"likes": db.lrange(f"likes:{user_id}:list", 0, -1)}

# return list of top 10 popular posts
@hug.get("/likes/popular", output=hug.output_format.pretty_json)
def get_popular(response, db: _redis):
  return {"likes": db.zrevrange('leaderboard', 0, 10)}
