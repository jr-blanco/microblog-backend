import boto3
import greenstalk
import json

db = boto3.resource('dyanmodb', endpoint_url='http://localhost:8000').Table("Polls")
client = greenstalk.Client(('127.0.0.1', 11300), use='email', watch='polls')

while True:
  job = client.reserve()
  data = json.loads(job.body)

  