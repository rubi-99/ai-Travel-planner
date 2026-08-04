import os
from typing import TypedDict, Annotated


import psycopg
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)

from langchain_groq import ChatGroq

from app.tools.tavily_tool import tavily_search
from app.tools.flight_tool import search_flights

from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(model= "llama-3.3-70b-versatile" )
DATABASE_URL = os.getenv("DATABASE_URL")

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage],add_messages]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return{
        "flight_results":flight_data,
        "messages" : [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls":state.get("llm_calls",0)+1
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
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Response Agent
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


graph_builder = StateGraph(TravelState)

#adding the node
graph_builder.add_node("flight_agent", flight_agent)
graph_builder.add_node("hotel_agent", hotel_agent)
graph_builder.add_node("itinerary_agent", itinerary_agent)
graph_builder.add_node("final_agent", final_agent)

#adding the edges
graph_builder.add_edge(START, "flight_agent")
graph_builder.add_edge("flight_agent", "hotel_agent")
graph_builder.add_edge("hotel_agent", "itinerary_agent")
graph_builder.add_edge("itinerary_agent", "final_agent")
graph_builder.add_edge("final_agent", END)

if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_rubi"
        }
    }

    user_input = input("Enter travel request: ")

    with PostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
        checkpointer.setup()

        graph = graph_builder.compile(checkpointer=checkpointer)

        result = graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ],
                    "user_query": user_input,
                    "flight_results": "",
                    "hotel_results": "",
                    "itinerary": "",
                    "llm_calls": 0
                },
                config=config
            )

        print("\nFINAL RESPONSE:\n")
        for msg in result["messages"]:
            print(msg.content)
        



    

    
