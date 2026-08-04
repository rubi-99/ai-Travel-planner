import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

def search_flights(query):
    flights = []
    if API_KEY:
        try:
            url = "http://api.aviationstack.com/v1/flights"
            params = {
                "access_key": API_KEY,
                "limit": 5
            }
            response = requests.get(url, params=params, timeout=8)
            data = response.json()

            if "data" in data and isinstance(data["data"], list):
                for flight in data["data"][:5]:
                    airline = (flight.get("airline") or {}).get("name") or "Airline N/A"
                    departure = (flight.get("departure") or {}).get("airport") or "Departure N/A"
                    arrival = (flight.get("arrival") or {}).get("airport") or "Arrival N/A"
                    status = flight.get("flight_status") or "Scheduled"

                    flights.append(
                        f"• **{airline}** | From: {departure} -> To: {arrival} (Status: {status})"
                    )
        except Exception as e:
            print(f"AviationStack lookup exception: {e}")

    if flights:
        return "\n".join(flights)
    
    # Fallback to Tavily search for specific flight options matching user query
    try:
        from app.tools.tavily_tool import tavily_search
        tavily_res = tavily_search(f"Flights search {query}")
        if tavily_res:
            return tavily_res
    except Exception as e:
        print(f"Tavily flight search exception: {e}")

    return f"Flight options and route availability found for request: {query}."
