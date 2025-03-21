# Import necessities 
import streamlit as st
from google import genai
import pandas as pd
import json

# Load JSON dataset
def load_data():
    return pd.read_csv("/Users/xanvelaa/Documents/crowdcast-api/train_data.csv")

data = load_data()
df = pd.DataFrame(data)

# Compute crowded months
median_tourists = df["tourists"].median()
df["crowded"] = df["tourists"] > median_tourists

# Define activity preferences
activity_preferences = {
    "surfing": {"days_sunny": 1, "days_cloudy": 0.5, "days_rained": -1},
    "hiking": {"days_sunny": 1, "days_cloudy": 0, "days_rained": -2},
    "staycation": {"days_sunny": -0.5, "days_cloudy": 1, "days_rained": 0.5},
}

# Compute scores
for activity in activity_preferences:
    df[f"{activity}_score"] = df.apply(lambda row: sum(
        row[key] * weight for key, weight in activity_preferences[activity].items()
    ), axis=1)


# Streamlit UI
st.title("🌴 Best Travel Time Recommender")
month = st.selectbox("Select a month:", df["month"])
activity = st.selectbox("Select an activity:", ["surfing", "hiking", "staycation"])

# Get selected month data
selected_data = df[df["month"] == month].iloc[0]

# Generate prompt for LLM
prompt = f"""
You are a travel planner. Your goal is to recommend whether or not
a person should go to Boracay on a specific month. Take note that if
it's too crowded, the user might not want to go to Boracay. However, if it's
just rainy and not overcrowded, you can assume that a user is still open
to a staycation at a hotel or resort. If your answer is no, recommend
another month for the user to go to in order to enjoy their selected 
activity.

The user wants to go {activity} in month {month}. Based on:
- Days Rained: {selected_data['days_rained']}
- Days Cloudy: {selected_data['days_cloudy']}
- Days Sunny: {selected_data['days_sunny']}
- Tourist Crowds: {"High" if selected_data['crowded'] else "Low"}

Should I go to Boracay on that month? Explain briefly.

"""

client = genai.Client(api_key="Input your API key here")
if st.button("Get Recommendation"):
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents = prompt)
    st.write(response.text)
