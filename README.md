# ✈️ AI Travel Booking & Planning System

An enterprise-grade, multi-agent travel planning system built with **LangGraph**, **Groq (LLaMA 3.3 70B)**, **Tavily Search**, **AviationStack**, and **Streamlit**.

---

## 🏗️ System Architecture

### Overview
The application follows a **Graph-based Multi-Agent Architecture** powered by **LangGraph**. User requests are passed through a stateful graph where specialized AI agents collaborate sequentially to validate, search, synthesize, and assemble a complete travel plan.

```mermaid
flowchart TD
    A[👤 User Input: Web UI / CLI] --> B[State Initialization: TravelState]
    B --> C[🛡️ Guardrail Agent]
    
    C -->|Intent Check| D{Is Query Travel-Related?}
    
    D -->|❌ No| E[🚫 Reject & Display Informative Message]
    E --> END[🏁 End Execution]
    
    D -->|✅ Yes| F[✈️ Flight Agent]
    F -->|Fetch Flight Options| G[🏨 Hotel Agent]
    G -->|Search Best Accommodations| H[🗓️ Itinerary Agent]
    H -->|Synthesize Day-by-Day Plan| I[🧠 Final Agent]
    I -->|Assemble Complete Plan| J[📊 Render Dashboard & Auto-Save MD]
    J --> END
```

---

## 📂 Project Directory Structure

```
ai-travel-planner/
│
├── app/
│   ├── __init__.py
│   ├── state.py         # Defines TravelState TypedDict schema
│   ├── agents.py        # Implementation of Guardrail, Flight, Hotel, Itinerary & Final agents
│   ├── graph.py         # LangGraph workflow compiler with PostgresSaver / MemorySaver checkpointer
│   ├── main.py          # Command-Line Interface (CLI) entrypoint
│   └── tools/
│       ├── __init__.py
│       ├── flight_tool.py  # Route-specific flight search tool
│       └── tavily_tool.py  # Tavily web search integration
│
├── travel_plans/        # Auto-saved Markdown travel plans
├── frontend.py          # Interactive Streamlit Web Dashboard
├── pyproject.toml       # Dependencies & project configuration
└── README.md            # System documentation & setup guide
```

---

## 🧩 Component Breakdown

### 1. **State Management (`app/state.py`)**
- **`TravelState`**: A centralized, type-annotated dictionary that persists across all agent nodes:
  - `user_query`: Raw request submitted by the user.
  - `is_travel_related`: Boolean flag set by `guardrail_agent`.
  - `flight_results`: Structured flight options synthesized by `flight_agent`.
  - `hotel_results`: Recommended hotel accommodations synthesized by `hotel_agent`.
  - `itinerary`: Day-by-day travel plan built by `itinerary_agent`.
  - `messages`: Conversation history (`HumanMessage`, `AIMessage`, `SystemMessage`).
  - `llm_calls`: Metric counter tracking total LLM invocations.

### 2. **Multi-Agent Pipeline (`app/agents.py`)**
- **🛡️ Guardrail Agent (`guardrail_agent`)**:
  - Uses Groq LLaMA 3.3 70B to evaluate whether the query is strictly related to travel.
  - Intercepts and rejects non-travel queries (e.g. general coding requests, math problems) upfront without executing downstream agents.
- **✈️ Flight Agent (`flight_agent`)**:
  - Executes route-targeted search via `search_flights` to find real airlines, direct/connecting routes, flight durations, and price estimates.
  - Synthesizes flight details for the exact origin and destination requested.
- **🏨 Hotel Agent (`hotel_agent`)**:
  - Uses `tavily_search` to find top-rated hotels, boutique stays, and resorts matching the user's budget and destination.
- **🗓️ Itinerary Agent (`itinerary_agent`)**:
  - Combines flight schedules, hotel options, and user budget to construct a comprehensive day-by-day travel itinerary.
- **🧠 Final Agent (`final_agent`)**:
  - Assembles all agent outputs into a polished, executive travel plan summary.

### 3. **Graph Orchestration & Persistence (`app/graph.py`)**
- Uses **LangGraph** `StateGraph` to manage control flow and conditional routing (`route_intent`).
- **State Checkpointer**: Features automatic dual-mode persistence:
  - Connects to **PostgreSQL** via `PostgresSaver` when `DATABASE_URL` is available.
  - Falls back seamlessly to in-memory `MemorySaver` if PostgreSQL is not running.

### 4. **User Interfaces**
- **Streamlit Web Dashboard (`frontend.py`)**: Modern, dark-themed UI featuring quick destination chips, live agent pipeline status, metric counters, custom Markdown rendering, and one-click plan downloads.
- **CLI (`app/main.py`)**: Terminal interface for command-line interaction.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.12+** | Core programming language |
| **LangGraph** | Multi-agent state machine and workflow orchestration |
| **Groq (LLaMA 3.3 70B)** | High-speed LLM inference engine |
| **Tavily Search API** | Real-time web search engine for flights and hotels |
| **AviationStack API** | Flight data integration |
| **PostgreSQL / psycopg** | Persistent checkpoint storage for user sessions |
| **Streamlit** | Interactive Web UI framework |

---

## 🚀 Setup & Execution

### 1. Environment Configuration
Ensure your `.env` file contains valid API keys:
```env
GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
AVIATIONSTACK_API_KEY="your_aviationstack_api_key"
DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_planner" # Optional
```

### 2. Run Web Dashboard (Streamlit)
```powershell
streamlit run frontend.py
```

### 3. Run Command-Line Interface (CLI)
```powershell
python -m app.main
```
