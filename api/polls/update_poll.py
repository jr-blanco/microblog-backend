from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal


def get_poll(user, question, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    try:
        response = table.get_item(Key={'user': user, 'question': question})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Response:')
        print(response, '\n\n\n')
        return response['Item']


def update_poll(user, question, option, voter, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Polls')

    response = table.update_item(
        Key={
            'user': user,
            'question': question
        },
        UpdateExpression=f"set info.scores[{option}] = info.scores[{option}] + :r, voters = list_append(voters, :v)",
        ConditionExpression="",
        ExpressionAttributeValues={
            ':r': Decimal(1),
            ':v': [voter]
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


if __name__ == '__main__':
    poll = update_poll(1, "Adipisicing ex nisi occaecat pariatur ex sint est sint.", 1, 2)
    if poll:
        print("Get poll succeeded:")
        pprint(poll, sort_dicts=False)
