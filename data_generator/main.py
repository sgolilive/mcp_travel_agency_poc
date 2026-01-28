from dotenv import load_dotenv

from data_generator import hotels
from db.airport_xfer_mongo_client import XferMongoClient
from db.attractions_mongo_client import AttractionsMongoClient
from db.flights_mongo_client import FlightsMongoClient
from db.hotels_mongo_client import HotelsMongoClient
from db.hubs_mongo_client import HubsMongoClient
from flights import generate_flight_data
from hotels import generate_hotel_data
from airport_transfers import generate_airport_transfers
from attractions import generate_local_attractions
from hubs import generate_hubs_data

load_dotenv()

if __name__ == "__main__":
    airports = FlightsMongoClient()
    hubs = HubsMongoClient()
    flights = FlightsMongoClient()
    xfers = XferMongoClient()
    hotels = HotelsMongoClient()
    attractions = AttractionsMongoClient()

    generate_hubs_data(hubs_collection=hubs)
    generate_airport_transfers(hubs=hubs, xfers=xfers)
    generate_flight_data(hubs=hubs, flights=flights)
    generate_hotel_data(hubs=hubs, hotels=hotels)
    generate_local_attractions(hubs=hubs, attractions=attractions)