import boto3

def delete_poll_table(dynamodb=None):
  if not dynamodb:
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

  table = dynamodb.Table('Polls')
  table.delete()

if __name__ == '__main__':
  delete_poll_table()
  print("Polls Table Deleted")