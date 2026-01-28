import os
import pymongo
from bson import ObjectId

from logger import get_logger

class TravelMongoClient:
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("MONGO_DB_NAME")]
        self.collection = self.db[collection_name]
        self.collection_name = collection_name

        self.logger = get_logger(collection_name)

    def insert_records(self, data):
        if data:
            self.logger.info(f"Inserting data into {self.collection_name}")
            self.collection.delete_many({})
            result = self.collection.insert_many(data)
            self.logger.info(f"🌍 Successfully inserted {len(result.inserted_ids)} {self.collection_name.replace('_', ' ')}")
        else:
            self.logger.warn(f"No data inserted into {self.collection_name}")

    def find_by_id(self, the_id: str):
        return self.collection.find_one({"_id": the_id if the_id.startswith("TRIP") else ObjectId(the_id)})