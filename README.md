# ✈️ AI Travel Booking & Planning System

An AI-powered multi-agent travel planning application built with **LangGraph**, **Groq (LLaMA 3.3 70B)**, **Tavily Search**, **AviationStack**, and **Streamlit**.

---

## 🛠️ Prerequisites & Setup

1. Environment variables are set in `.env`:
   - `GROQ_API_KEY`: Groq API Key
   - `TAVILY_API_KEY`: Tavily Search API Key
   - `AVIATIONSTACK_API_KEY`: AviationStack Flight API Key
   - `DATABASE_URL`: PostgreSQL connection string (optional; falls back gracefully to `MemorySaver` if PostgreSQL is not running)

---

## 🚀 How to Run

### 1. Web UI (Streamlit)
To launch the interactive web dashboard:

```bash
streamlit run frontend.py
```
*(Or if using the local virtual environment: `.venv\Scripts\streamlit run frontend.py` or `uv run streamlit run frontend.py`)*

### 2. Command Line Interface (CLI)
To run the terminal interface:

```bash
python -m app.main
```
*(Or if using the local virtual environment: `.venv\Scripts\python -m app.main` or `uv run python -m app.main`)*

---

## 🤖 Multi-Agent Pipeline

1. **✈️ Flight Agent**: Queries flight schedules & search APIs.
2. **🏨 Hotel Agent**: Searches for recommended hotels & accommodations using web search.
3. **🗓️ Itinerary Agent**: Synthesizes flight & hotel data into a day-by-day travel itinerary.
4. **🧠 Final Agent**: Assembles the complete travel plan with metrics and summary.
