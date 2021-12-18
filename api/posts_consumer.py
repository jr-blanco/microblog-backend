import greenstalk
import json
import sqlite_utils

# Connect and consume jobs
client = greenstalk.Client(('127.0.0.1', 11300))
worker = greenstalk.Client(('127.0.0.1', 11300), use='polls')

print("Using tube: ", client.using())
print("Watching tube: ", client.watching())
db = sqlite_utils.Database("./var/timelines.db")
posts = db["posts"]

# infine loop
while True:
  # consume a job
  job = client.reserve()
  # load data
  data = json.loads(job.body)
  print(data)
  # write to database
  try:
    posts.insert(data)
    data['id'] = posts.last_pk
  except Exception as e:
    print('Error adding to post database from consume')
  print("Successfully Added a new post from consume.")

  # send to polls worker to check if text has a valid poll URL
  worker.put(json.dumps[data])
  
  # delete job
  client.delete(job)
