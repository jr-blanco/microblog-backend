import configparser
import logging.config
from hug import authentication
import requests
import json
import boto3
from pprint import pprint

import hug

# Load configuration
config = configparser.ConfigParser()
config.read("./etc/posts_api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# Arguements to inject into route functions
@hug.directive()
def boto(section="boto3", key="dbfile", **kwargs):
  return boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

@hug.directive()
def log(name=__name__, **kwargs):
  return logging.getLogger(name)

# Routes
#
