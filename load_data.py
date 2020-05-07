'''
A file to load the data from the json file to the mySQL database.
After a one time run the dictionary can be used.
'''

import sqlalchemy
import json
import pprint
import os

user = os.environ['USER']
pw = os.environ['PW']

engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{pw}@localhost/Dictionary')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

newTable = sqlalchemy.Table('dict', metadata, autoload=True, autoload_with=engine)

with open("data.json", "r") as file:
    data = json.load(file)

for key in data:
    for value in data.get(key):
        query = sqlalchemy.insert(newTable).values(word=key, definition=value)
        result_proxy = connection.execute(query)

