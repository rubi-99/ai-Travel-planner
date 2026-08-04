import os
from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.postgres import PostgreSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage
)