from decimal import Decimal
import json
from os import write
import boto3
from lorem_text import lorem
from faker import Faker
import random


def write_json(data, filename='data.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["polls"].append(data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=2)


def json_file_generator(num):
    fake = Faker()
    data = {}
    for i in range(num + 1):
        data['user'] = i
        data['question'] = fake.sentence()
        temp = {}
        temp['voters'] = {}
        for j in range(random.randint(2, 4)):
            temp[fake.word()] = {
                'score': 0
            }
        data['responses'] = temp
        write_json(data)
        temp.clear()
        data.clear()


if __name__ == '__main__':
    json_file_generator(100)
