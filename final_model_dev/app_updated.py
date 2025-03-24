# Import necessities 
import streamlit as st
from google import genai
import pandas as pd
import json

# Load CSV dataset
user_root = "/Users/xanvelaa/Desktop/"

# Load dataset
def load_data():
    return pd.read_csv(user_root + "llm_dataset.csv")  

df = load_data()

# Streamlit UI
st.title("🌴 Best Travel Time Recommender")

# User selects location, month, and activity
location = st.selectbox("Select a location:", df["location"].unique())
month = st.selectbox("Select a month:", df["month"].unique())
activity = st.selectbox("Select an activity:", ["Water Sports", "Hiking", "Staycation", "Nightlife"])

# Get selected month and location data
selected_data = df[(df["location"] == location) & (df["month"] == month)].iloc[0]

# Generate prompt for LLM
prompt = f"""
You are a travel planner. Your goal is to recommend whether or not
a person should go to {location} on a specific month. Take note that if
it's too crowded, the user might not want to go there. However, if it's
just rainy and not overcrowded, you can assume that a user is still open
to a staycation at a hotel or resort. If your answer is no, recommend
another month for the user to go to in order to enjoy their selected 
activity.

The user wants to go {activity} in {location} during the month of {month}. Based on:
- Days Rained: {selected_data['days_rained']}
- Days Cloudy: {selected_data['days_cloudy']}
- Days Sunny: {selected_data['days_sunny']}
- Tourist Crowds: {"High" if selected_data['crowded'] else "Low"}

Should I go to {location} on that month? Explain briefly.
"""

client = genai.Client(api_key="api_key")
if st.button("Get Recommendation"):
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents = prompt)
    st.write(response.text)