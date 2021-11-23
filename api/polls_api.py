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
