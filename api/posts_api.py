import configparser
import logging.config
from hug import authentication
import requests
import json
import greenstalk
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
def greenstalkjob(url='127.0.0.1', port=11300, **kwargs):
  return greenstalk.Client((url, port))

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
def home_timeline(request, db: sqlite, user: hug.directives.user):
  # get the users this user is following
  posts = []
  if "username" in request.params and request.params["username"] == user:
    r = requests.get(f"http://localhost:5000/following/{request.params['username']}")
    data = r.json()['following']

    for follower in data:
      posts.extend(list(db["posts"].rows_where("username = ?", [follower['friendname']], limit=5)))
    
  return {"posts": sorted(posts, key=lambda x: x['timestamp'], reverse=True)}
      
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

# create a new post
@hug.post("/timelines/posts/", status=hug.falcon.HTTP_201, requires=authentication)
def create_post(
  response,
  username: hug.types.text,
  text: hug.types.text,
  db: sqlite,
):
  posts = db["posts"]

  post = {
    "username": username,
    "text": text,
  }

  try:
    posts.insert(post)
    post["id"] = posts.last_pk
  except Exception as e:
    response.status = hug.falcon.HTTP_409
    return {"error": str(e)}

  response.set_header("Location", f"/timelines/public/{post['id']}")
  return post

# insert a new job
@hug.post("/timelines/posts/jobs", status=hug.falcon.HTTP_202)
def insert_job(
  response,
  username: hug.types.text,
  text: hug.types.text,
  jobs: greenstalkjob,
):
  body = json.dumps({
    'username': username,
    'text': text,
  })
  jobs.put(body)