import os
from pathlib import Path

import pymongo
import pytoml


class DBHandler:
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        with open(Path(os.getcwd()) / "pyproject.toml", "r") as f:
            project_config = pytoml.load(f)
            self.db = self.client[project_config.get('project').get('name')]
        self.collection = self.db[collection_name]

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def update(self, query, new_data):
        self.collection.update_one(query, new_data)

    def delete(self, query):
        self.collection.delete_one(query)
