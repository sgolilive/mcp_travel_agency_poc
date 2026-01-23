from dotenv import load_dotenv
from flights import Flights
from hotels import Hotels
from local_attractions import LocalAttractions
from airport_transfers import AirportTransfer

load_dotenv()

if __name__ == "__main__":
    flights = Flights()
    hotels = Hotels()
    local_attractions = LocalAttractions()
    airport_transfers = AirportTransfer()

    flights.generate_flight_data()
    hotels.generate_hotel_data()
    local_attractions.generate_local_experiences()
    airport_transfers.generate_airport_transfers()