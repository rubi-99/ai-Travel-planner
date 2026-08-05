from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    is_travel_related: bool
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
