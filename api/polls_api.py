import configparser
import logging.config
import boto3
from boto3.dynamodb.conditions import Key
from pprint import pprint
from falcon import response

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
# Returns the 
@hug.get("/polls/users/{user_id}", output=hug.output_format.pretty_json)
def get_user_polls(
  response,
  user_id: hug.types.number,
  db: boto
):
  response = db.query(
    KeyConditionExpression=Key('user').eq(user_id)
  )
  return response['Items']
