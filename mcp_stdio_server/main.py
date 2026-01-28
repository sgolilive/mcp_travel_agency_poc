from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from db.airport_xfer_mongo_client import XferMongoClient
from db.attractions_mongo_client import AttractionsMongoClient
from db.flights_mongo_client import FlightsMongoClient
from db.hotels_mongo_client import HotelsMongoClient
from db.hubs_mongo_client import HubsMongoClient
from tools.travel_resources import TravelResources
from tools.travel_service import TravelServiceDeps, TravelService

load_dotenv(verbose=True)

def get_deps():
    hubs = HubsMongoClient()
    flights = FlightsMongoClient()
    hotels = HotelsMongoClient()
    xfers = XferMongoClient()
    attractions = AttractionsMongoClient()
    return TravelServiceDeps(hubs=hubs, flights=flights, hotels=hotels, attractions=attractions, transfers=xfers, mcp=FastMCP(name="travel_agency"))

# use this command for testing using mcp inspector
# export PYTHONPATH=$PYTHONPATH:.
# npx @modelcontextprotocol/inspector python main.py
def run_mcp_using_stdio(mcp):
    mcp.run(transport="stdio")

#register all mcp tools here by scanning the provided service.
def register_tools(mcp, service, resources):
    import inspect

    for _, method in inspect.getmembers(service, predicate=inspect.iscoroutinefunction):
        if getattr(method, "_is_mcp_tool", False):
            mcp.tool()(method)

    mcp.resource('docs://policies/{topic}')(resources.get_policy)
    # mcp.resource('list://airports/{country}/supported', resources.get_airports_by_country)
    mcp.resource('list://countries/supported')(resources.get_countries)
    # mcp.resource('list://attractions/{city}', resources.get_attractions)
    # mcp.resource('list://hotels/{city}', resources.get_hotels_at_destination_city)

def create_mcp_server():
    deps = get_deps()
    travel_service = TravelService(deps)
    travel_resource = TravelResources(deps)
    register_tools(deps.mcp, travel_service, travel_resource)

    return deps.mcp

if __name__ == '__main__':
    mcp_server = create_mcp_server()
    run_mcp_using_stdio(mcp_server)