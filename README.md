# Trip Planner Agent (MCP-style)

An **LLM travel planning agent** with Streamlit UX that combines **Gemini** reasoning with **real-time data**: weather (OpenWeatherMap), flights and hotels (Amadeus), and points of interest.

## Features

- **One-shot prompts** like *"Plan a 3-day trip to Tokyo in May"* or *"Plan a 2-day trip to Udaipur in May"*
- **Structured output**: city culture paragraph, current weather & forecast, travel dates, flight options, hotel options, day-by-day trip plan
- **Tools**: Weather API, Flight search (Amadeus), Hotel list (Amadeus), Points of interest (Amadeus), city culture (LLM)
- **Framework**: LangChain + LangGraph (ReAct agent), **LLM**: Google Gemini

## Quick start

### 1. Clone and install

```bash
cd /path/to/project
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API keys

Copy `.env.example` to `.env` and fill in at least **GOOGLE_API_KEY** (required). Optional: OpenWeatherMap and Amadeus for live weather, flights, and hotels.

```bash
cp .env.example .env
# Edit .env:
# GOOGLE_API_KEY=...        # Required. Get at https://aistudio.google.com/apikey
# OPENWEATHER_API_KEY=...   # Optional. Get at https://openweathermap.org/api
# AMADEUS_CLIENT_ID=...      # Optional. Get at https://developers.amadeus.com/register
# AMADEUS_CLIENT_SECRET=...
# DEFAULT_ORIGIN=DEL         # Optional. Default origin for flight search (IATA code)
```

### 3. Run the app

```bash
streamlit run app.py
```

Open the URL shown (e.g. `http://localhost:8501`). Use the sample prompts in the sidebar or type your own (e.g. *Plan a 3-day trip to Tokyo in May*).

## Expected output

For prompts like *"Plan a 3-day trip to Tokyo in May"* or *"Plan a 2-day trip to Udaipur in May"*, the agent returns:

1. **One paragraph** on the city’s cultural and historic significance  
2. **Current weather** and **weather forecast** for the trip dates  
3. **Travel dates** (e.g. May 15–17, 2025)  
4. **Flight options** (origin → destination, dates, sample prices/times)  
5. **Hotel options** in the city  
6. **Day-by-day trip plan** (itinerary with suggested activities)

## Tech stack

| Component        | Choice                          |
|-----------------|----------------------------------|
| Framework       | LangChain + LangGraph           |
| LLM             | Google Gemini (e.g. gemini-1.5-flash) |
| UX              | Streamlit                       |
| Weather         | OpenWeatherMap (geocoding + current + 5-day forecast) |
| Flights         | Amadeus Flight Offers Search    |
| Hotels          | Amadeus Reference Data (hotel list) |
| Places / POI    | Amadeus Points of Interest (Google Places–style) |

## Project layout

- `app.py` – Streamlit UI and agent invocation  
- `agent.py` – ReAct agent (Gemini + tools, system prompt)  
- `tools.py` – Tool implementations (weather, flights, hotels, POI, culture hint)  
- `requirements.txt` – Python dependencies  
- `.env.example` – Example env vars for API keys  

## Submit checklist

- **URL**: Run locally with `streamlit run app.py` and use the local URL, or deploy (e.g. Streamlit Community Cloud) and submit that URL.  
- **Screenshots**: Capture 1–2 screens showing a sample prompt (e.g. Tokyo or Udaipur) and the agent’s full response (culture, weather, dates, flights, hotels, trip plan).

## Notes

- Without **OPENWEATHER_API_KEY**, weather tools return a friendly “not configured” message; the rest of the plan still runs.  
- Without **Amadeus** keys, flight and hotel tools return “not configured”; the agent still produces culture, dates, and an itinerary from the LLM.  
- **DEFAULT_ORIGIN** (e.g. `DEL`, `LON`, `NYC`) is used when the user doesn’t specify an origin for flight search.
