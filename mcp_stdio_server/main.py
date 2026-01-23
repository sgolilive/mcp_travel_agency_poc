from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from data_generator.airport_transfers import AirportTransfers
from data_generator.flights import Flights
from data_generator.hotels import Hotels
from data_generator.local_attractions import LocalAttractions
from tools.travel_service import TravelServiceDeps, TravelService

load_dotenv(verbose=True)

def get_deps():
    flights = Flights()
    hotels = Hotels()
    xfers = AirportTransfers()
    attractions = LocalAttractions()
    return TravelServiceDeps(flights=flights, hotels=hotels, mcp=FastMCP(name="travel_agency"), attractions=attractions, transfers=xfers)

# use this command for testing using mcp inspector
# export PYTHONPATH=$PYTHONPATH:.
# npx @modelcontextprotocol/inspector python main.py
def run_mcp_using_stdio(mcp):
    mcp.run(transport="stdio")

#register all mcp tools here by scanning the provided service.
def register_tools(mcp, service):
    import inspect

    for _, method in inspect.getmembers(service, predicate=inspect.iscoroutinefunction):
        if getattr(method, "_is_mcp_tool", False):
            mcp.tool()(method)

def create_mcp_server():
    deps = get_deps()
    travel_service = TravelService(deps)

    register_tools(deps.mcp, travel_service)

    return deps.mcp

if __name__ == '__main__':
    mcp_server = create_mcp_server()
    run_mcp_using_stdio(mcp_server)