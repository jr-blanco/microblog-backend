import configparser
import logging.config
import boto3
from pprint import pprint

import hug

# Load configuration
config = configparser.ConfigParser()
config.read("./etc/polls_api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)

# Arguements to inject into route functions
@hug.directive()
def boto(url="http://localhost:8000", table="Polls", **kwargs):
  return boto3.resource('dynamodb', endpoint_url=url).Table(table)

@hug.directive()
def log(name=__name__, **kwargs):
  return logging.getLogger(name)

# Routes
#
@hug.get()
