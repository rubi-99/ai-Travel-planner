import os
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import TravelState
from app.agents import (
    flight_agent,
    hotel_agent,
    itinerary_agent,
    final_agent
)

DATABASE_URL = os.getenv("DATABASE_URL")

def build_graph():
    graph_builder = StateGraph(TravelState)

    # Add agent nodes
    graph_builder.add_node("flight_agent", flight_agent)
    graph_builder.add_node("hotel_agent", hotel_agent)
    graph_builder.add_node("itinerary_agent", itinerary_agent)
    graph_builder.add_node("final_agent", final_agent)

    # Add edges
    graph_builder.add_edge(START, "flight_agent")
    graph_builder.add_edge("flight_agent", "hotel_agent")
    graph_builder.add_edge("hotel_agent", "itinerary_agent")
    graph_builder.add_edge("itinerary_agent", "final_agent")
    graph_builder.add_edge("final_agent", END)

    # Setup Checkpointer: Try PostgresSaver, fall back to MemorySaver
    checkpointer = None
    if DATABASE_URL:
        try:
            from psycopg_pool import ConnectionPool
            from langgraph.checkpoint.postgres import PostgresSaver
            pool = ConnectionPool(conninfo=DATABASE_URL, max_size=10, kwargs={'autocommit': True})
            checkpointer = PostgresSaver(pool)
            checkpointer.setup()
        except Exception as e:
            print(f"Postgres checkpointer notice ({e}). Falling back to MemorySaver.")
            checkpointer = MemorySaver()
    else:
        checkpointer = MemorySaver()

    return graph_builder.compile(checkpointer=checkpointer)
