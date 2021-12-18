import greenstalk
import json
import redis
from requests.api import post


client = greenstalk.Client(('127.0.0.1', 11300), use='likes', watch="likes")
print("Using tube: ", client.using())
print("Watching tube: ", client.watching())
db = redis.Redis(host='localhost', port=6379, db=0)

while True:
  job = client.reserve()
  data = json.loads(job.body)
  post_id = data['post_id']
  user_id = data['user_id']
  amount = data['amount']

  if db.exists(f"posts:{post_id}:likes"):
    db.incr(f'posts:{post_id}:likes', amount)
    db.rpush(f'users:{user_id}:likes', post_id)
    num = db.get(f'posts:{post_id}:likes')
    db.zadd('leaderboard', {post_id: num})
  client.delete(job)