import smtplib
import greenstalk
import json

# connections
client = greenstalk.Client(('127.0.0.1', 11300), watch='email')
server = smtplib.SMTP('localhost', 1025)
server.set_debuglevel(1)

# Constants
FROM = 'company@company.com'

while True:
  job = client.reserve()
  data = json.load(job.body)
  server.sendmail(FROM, data['username'], data['message'])
  client.delete(job)

