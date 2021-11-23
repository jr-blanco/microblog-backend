from decimal import Decimal
import json
import boto3


def load_polls(polls, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')
    for poll in polls:
        user = int(poll['user'])
        question = poll['question']
        print("Adding Poll:", user, question)
        table.put_item(Item=poll)


if __name__ == '__main__':
    with open("./share/poll.json") as json_file:
        poll_list = json.load(json_file, parse_float=Decimal)
    load_polls(poll_list)