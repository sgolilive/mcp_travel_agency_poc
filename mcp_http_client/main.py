import asyncio
import random
import re

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import os
from dotenv import load_dotenv
from logger import get_logger

load_dotenv() # Load environment variables
agent_state = {}
logger = get_logger(__name__)

def extract_trip_id(response):
    text = response.content[0].text

    match = re.search(r"trip_id='(TRIP-[A-Z0-9]+)'", text)
    trip_id = match.group(1)
    return trip_id

def unpack_response(response) -> str:
    import json

    if response.isError:
        logger.error(response.content)
        return ""

    text = response.content[0].text
    data = json.loads(text)

    logger.info(data)
    agent_state['trip_id'] = data['trip_id']

    return data['message']

def pick_random_flight(message: str):
    flight_ids = re.findall(r"REF:\s*([a-f0-9]{24})", message)
    if not flight_ids:
        raise ValueError("No flights found to select from")
    agent_state['flight_id'] = random.choice(flight_ids)

def pick_random_hotel(message: str):
    pattern = re.compile(
        r"REF:\s*([a-f0-9]{24}).*?Room Type:\s*(\w+)",
        re.DOTALL
    )

    matches = pattern.findall(message)

    if not matches:
        raise ValueError("No hotels found")

    hotel_id, room_type = random.choice(matches)

    agent_state['hotel_id'] = hotel_id
    agent_state['room_type'] = room_type

async def run_client(url: str):
    # Connect to the streamable HTTP server using an async context manager
    async with streamable_http_client(url) as streams:
        recv_stream, send_stream, _get_session_id = streams
        # Create an MCP session
        async with ClientSession(recv_stream, send_stream) as session:
            await session.initialize() # Initialize the session with the server
            print(f"✅ Connected to server: {url}")

            #1. greet customer to get the trip id
            response = await session.call_tool('greet_customer', {'name': 'Shamukhi'})
            unpack_response(response)

            #2. search flights to get started
            response = await session.call_tool('search_flights', {
                "origin": "BOM",
                "destination": "DXB",
                "travel_date": "2026-01-23",
                "trip_id": agent_state["trip_id"]
            })

            message = unpack_response(response)

            if 'no flights found' in message:
                logger.error(message)
                return

            #3.save flight details
            pick_random_flight(message)
            response = await session.call_tool('save_flight_details', {'trip_id': agent_state["trip_id"], 'flight_id': agent_state["flight_id"]})
            unpack_response(response)

            #4. find hotels
            response = await session.call_tool('search_hotels', {'trip_id': agent_state["trip_id"]})
            message = unpack_response(response)

            if 'no hotels found' in message:
                logger.error(message)
                return

            pick_random_hotel(message)
            response = await session.call_tool('save_hotel_details', {'trip_id': agent_state['trip_id'], 'hotel_id': agent_state["hotel_id"], 'room_type': agent_state["room_type"]})
            unpack_response(response)

            response = await session.call_tool('view_itinerary', {'trip_id': agent_state["trip_id"]})
            unpack_response(response)

            return

            # Discover and load tools exposed by the server
            # tools = await load_mcp_tools(session)
            # print(f"Tools available: {[t.name for t in tools]}")

            # Example of calling a server method/tool (if you have an agent/LLM)
            # You would typically integrate this with an AI model for tool usage.
            # print(await session.call_tool("your_tool_name", {"arg1": "value1"}))

if __name__ == "__main__":
    # Get server URL from environment or command line, e.g., "http://localhost:8000/mcp"
    server_url = os.getenv("MCP_SERVER_URL")
    asyncio.run(run_client(server_url))