import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
DEFAULT_ORIGIN = os.getenv("DEFAULT_ORIGIN", "DEL")

# =========================
# LLM USING OPENROUTER
# =========================
def generate_llm_response(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
        },
    )

    return response.json()["choices"][0]["message"]["content"]


# =========================
# WEATHER FUNCTION
# =========================
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if "list" not in response:
        return "Weather data unavailable."

    forecast = response["list"][:5]
    result = ""

    for item in forecast:
        date = item["dt_txt"]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"]
        result += f"{date} → {temp}°C, {desc}\n"

    return result


# =========================
# AMADEUS TOKEN
# =========================
def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_CLIENT_SECRET,
    }

    response = requests.post(url, data=data)
    return response.json().get("access_token")


# =========================
# FLIGHT SEARCH
# =========================
def get_flights(destination_code):
    token = get_amadeus_token()
    if not token:
        return "Flight API authentication failed."

    departure_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": DEFAULT_ORIGIN,
        "destinationLocationCode": destination_code,
        "departureDate": departure_date,
        "adults": 1,
        "max": 3,
    }

    response = requests.get(url, headers=headers, params=params).json()

    if "data" not in response:
        return "No flight data found."

    flights = []
    for offer in response["data"]:
        price = offer["price"]["total"]
        airline = offer["validatingAirlineCodes"][0]
        flights.append(f"Airline: {airline} | Price: {price}")

    return "\n".join(flights)


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.title("✈️ AI Travel Planner Agent")
st.write("Plan smart trips using AI + Real-Time APIs")

user_prompt = st.text_input("Example: Plan a 3-day trip to Tokyo in May")

if st.button("Generate Trip Plan"):

    if not user_prompt:
        st.warning("Please enter a travel request.")
    else:

        city = user_prompt.split("to")[-1].split("in")[0].strip()

        st.subheader("🌍 Cultural & Historical Overview")

        llm_prompt = f"""
        Provide one paragraph about the cultural and historical significance of {city}.
        Then create a structured 3-day itinerary with activities for each day.
        Include recommended travel dates in May.
        """

        llm_output = generate_llm_response(llm_prompt)
        st.write(llm_output)

        st.subheader("🌦 Current Weather Forecast")
        weather_info = get_weather(city)
        st.write(weather_info)

        st.subheader("✈️ Flight Options")

        # Manual IATA mapping
        city_codes = {
            "tokyo": "TYO",
            "udaipur": "UDR",
            "london": "LON",
            "new york": "NYC",
        }

        destination_code = city_codes.get(city.lower())

        if destination_code:
            flight_info = get_flights(destination_code)
        else:
            flight_info = "Flight search available for Tokyo, Udaipur, London, New York."

        st.write(flight_info)

        st.subheader("🏨 Hotel Suggestions")
        st.write("Top-rated central hotels, boutique heritage stays, and budget-friendly options are available in this city.")
