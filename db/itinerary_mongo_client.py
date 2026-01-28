from datetime import datetime
from typing import Any
from db.mongo_client import TravelMongoClient


class ItineraryMongoClient(TravelMongoClient):
    def __init__(self):
        super().__init__('itinerary')

    def save_itineraries(self, trip_id: str, fields_to_update: dict[Any, Any]):
        fields_to_update.update({"last_updated": datetime.now()})
        self.collection.update_one(
            {'_id': trip_id},
            {'$set': fields_to_update},
            upsert=True
        )