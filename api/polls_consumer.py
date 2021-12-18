import boto3
from boto3.dynamodb.conditions import Key
import greenstalk
import json
import re

db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000').Table("Polls")
client = greenstalk.Client(('127.0.0.1', 11300), use='email', watch='polls')
sqlJob = greenstalk.Client(('127.0.0.1', 11300), use='deletePost')

while True:
  job = client.reserve()
  data = json.loads(job.body)

  text = data['text']
  urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
  for url in urls:
    # validate url
    tree = url.split('/')
    question = tree[5].replace("%20", " ")
    response = db.query(
        IndexName="QuestionIndex",
        KeyConditionExpression=Key('question').eq(question)
    )
    if len(response['Items']) != 1:
      data['message'] = f"Invalid poll URL: {tree}\nPost was deleted!"
      sqlJob.put(json.dumps(data))
      break
  client.delete(job)
    