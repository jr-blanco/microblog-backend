import configparser
import logging.config

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