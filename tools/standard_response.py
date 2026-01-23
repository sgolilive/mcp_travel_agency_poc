import re
from functools import wraps

def standard_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        trip_id = kwargs.get("trip_id")
        try:
            result = await func(*args, **kwargs)

            # If the tool returned a list, join it
            if isinstance(result, list):
                result = "\n".join(result)
            elif isinstance(result, str):
                result = result
            elif isinstance(result, dict):
                # If tool already returns structured data
                return result
            else:
                result = str(result)

            # Centralized Trip ID footer
            if trip_id:
                return {
                    'message': result,
                    'trip_id': trip_id
                }

            match = re.search(r"trip_id='(TRIP-[A-Z0-9]+)'", result)
            if match:
                trip_id = match.group(1)
                return {
                    "message": result,
                    "trip_id": trip_id
                }

        except Exception as e:
            return {
                "error": True,
                "message": f"Error in {func.__name__}",
                "details": str(e)
            }

    return wrapper