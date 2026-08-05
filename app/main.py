from langchain_core.messages import HumanMessage
from app.graph import build_graph

def main():
    graph = build_graph()
    config = {
        "configurable": {
            "thread_id": "user_rubi"
        }
    }

    user_input = input("Enter travel request: ")

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "is_travel_related": True,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    if not result.get("is_travel_related", True):
        print("\n" + result["messages"][-1].content)
        return

    print("\nFINAL RESPONSE:\n")
    for msg in result["messages"]:
        print(msg.content)

if __name__ == "__main__":
    main()
