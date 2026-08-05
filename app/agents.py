import os
import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.state import TravelState
from app.tools.flight_tool import search_flights
from app.tools.tavily_tool import tavily_search
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

# Guardrail Agent
def guardrail_agent(state: TravelState):
    query = state["user_query"]
    prompt = f"""
    Analyze the following user query and determine if it is related to travel, trip planning, flight search, hotel accommodations, tourism, sightseeing, local attractions, or vacation budgeting.

    User Query: "{query}"

    Respond ONLY with a JSON object in this format:
    {{
      "is_travel": true or false,
      "reason": "short explanation"
    }}
    """
    
    is_travel = False
    try:
        response = llm.invoke([
            SystemMessage(content="You are a strict guardrail classifier for an AI Travel Planner application. Your job is to reject any non-travel request such as writing code, solving math problems, general knowledge questions, or non-travel tasks."),
            HumanMessage(content=prompt)
        ])
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        data = json.loads(content)
        is_travel = bool(data.get("is_travel", False))
    except Exception as e:
        # Fallback keyword validation if parsing fails
        keywords = ["travel", "trip", "flight", "hotel", "tour", "visit", "vacation", "airline", "stay", "resort", "destination", "itinerary", "places", "budget", "day", "days"]
        is_travel = any(kw in query.lower() for kw in keywords)

    if is_travel:
        return {
            "is_travel_related": True,
            "messages": [AIMessage(content="Query validated: Travel intent confirmed.")],
            "llm_calls": state.get("llm_calls", 0) + 1
        }
    else:
        rejection_msg = "🚫 **Non-Travel Query Detected**: I am an AI Travel Assistant designed exclusively to help with travel planning, flight options, hotel recommendations, and trip itineraries. Please enter a travel-related query (e.g., *'Plan a 5-day trip to Paris'* or *'Hotels in Tokyo'*)."
        return {
            "is_travel_related": False,
            "flight_results": "N/A - Non-travel request",
            "hotel_results": "N/A - Non-travel request",
            "itinerary": rejection_msg,
            "messages": [AIMessage(content=rejection_msg)],
            "llm_calls": state.get("llm_calls", 0) + 1
        }

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)

    prompt = f"""
    Based on the user's travel query and raw flight search data below, synthesize a clear, well-structured flight report specifically matching the requested origin and destination.

    User Query: "{query}"

    Raw Search Data:
    {flight_data}

    Provide:
    - Route Overview (Origin -> Destination)
    - Recommended Airlines (Direct vs Connecting)
    - Estimated Flight Duration
    - Estimated Ticket Price Range (per person and for total group in INR / Rs.)
    - Helpful Booking Tips
    """

    response = llm.invoke([
        SystemMessage(content="You are an expert flight search agent. Always extract and synthesize flight options matching the specific origin and destination in the user request. Do not include unrelated routes."),
        HumanMessage(content=prompt)
    ])

    return {
        "flight_results": response.content,
        "messages": [
            AIMessage(content="Flight results fetched and synthesized.")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = tavily_search(query)
    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):
    prompt = f"""
    Create a travel itinerary.
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}
    """
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner"),
        HumanMessage(content=prompt)
    ])
    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Agent
def final_agent(state: TravelState):
    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}
    """
    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
