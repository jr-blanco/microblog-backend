import boto3


def create_poll_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url=("http://localhost:8000"))

    table = dynamodb.create_table(
        TableName="Polls",
        KeySchema=[
            {
                'AttributeName': 'user',
                'KeyType': 'HASH'  # partition key
            },
            {
                'AttributeName': 'question',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'question',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'QuestionIndex',
                'KeySchema': [{
                    'AttributeName': 'question',
                    'KeyType': 'HASH'
                }],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }

            }
        ]
    )
    return table


if __name__ == '__main__':
    poll_table = create_poll_table()
    print("Table status:", poll_table.table_status)
