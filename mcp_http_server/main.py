from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from db.airport_xfer_mongo_client import XferMongoClient
from db.attractions_mongo_client import AttractionsMongoClient
from db.flights_mongo_client import FlightsMongoClient
from db.hotels_mongo_client import HotelsMongoClient
from db.hubs_mongo_client import HubsMongoClient
from tools.travel_service import TravelServiceDeps, TravelService

load_dotenv(verbose=True)

def get_deps():
    hubs = HubsMongoClient()
    flights = FlightsMongoClient()
    hotels = HotelsMongoClient()
    xfers = XferMongoClient()
    attractions = AttractionsMongoClient()
    return TravelServiceDeps(hubs=hubs, flights=flights, hotels=hotels, mcp=FastMCP(name="travel_agency"), attractions=attractions, transfers=xfers)

# use the following logic for stdio for console testing
# Run the inspector pointing to your local HTTP endpoint
# open two terminal windows:
# first 1: python mcp_http_server/mail.py + press enter
#         export PYTHONPATH=$PYTHONPATH:. + enter
# second one, # for running inspector:
#   npx @modelcontextprotocol/inspector http://127.0.0.1:9000/mcp
# in the browser make sure following settings
#   URL: http://127.0.0.1:9000/mcp
#   Proxy Address: http://localhost:6277
#   Proxy Token: pasted correctly
#       example: e575a1f0b1bc4bc5fbc8b840a2ecc7a87e16c88fc3bd1d2c8e5d279cb5cbaab3

def run_mcp_using_http(mcp):
    import uvicorn
    from fastapi.middleware.cors import CORSMiddleware

    app = mcp.streamable_http_app()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Inspector runs in browser
        allow_credentials=True,
        allow_methods=["*"],  # MUST allow OPTIONS
        allow_headers=["*"],
    )

    print("🚀 MCP Server running at http://127.0.0.1:9000/mcp")
    uvicorn.run(app, host="127.0.0.1", port=9000)

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
    run_mcp_using_http(mcp_server)