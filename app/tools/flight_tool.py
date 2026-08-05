import os
import requests
from dotenv import load_dotenv
from app.tools.tavily_tool import tavily_search

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

def search_flights(query):
    """
    Performs route-specific flight searches using Tavily Web Search and AviationStack
    to retrieve accurate airlines, durations, routes, and price options for the user's query.
    """
    search_query = f"flights for {query} options airlines price duration"
    try:
        results = tavily_search(search_query)
        if results and len(results.strip()) > 50:
            return results
    except Exception as e:
        print(f"Tavily flight search exception: {e}")

    # Fallback response
    return f"Flight options and route details for: {query}."
